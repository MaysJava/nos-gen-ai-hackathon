from pathlib import Path
import fitz

# Find the main project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Find the NOS document
PDF_PATH = PROJECT_DIR / "raw_data" / "document_to_anonymize.pdf"

# Open the PDF and extract its text
with fitz.open(PDF_PATH) as document:
    pages = [page.get_text(sort=True) for page in document]

text = "\n".join(pages)

# Display the extracted text
print(text)


import os
import requests
from dotenv import load_dotenv

# Load our secret API key from the .env file
load_dotenv(PROJECT_DIR / ".env")

# Get the API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("Gemini API key not found!")

# Gemini API endpoint
api_url = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.8-flash:generateContent"
)

# A simple test prompt
prompt = f"""
You are an expert in anonymising Portuguese medical documents.

Anonymise the document below by replacing sensitive personal information
with asterisks (*).


IMPORTANT FORMATTING RULES:
- Keep every original non-sensitive word exactly unchanged.
- Preserve commas, full stops, parentheses, colons, and other punctuation.
- Never rewrite or paraphrase sentences.
- Never delete words unless they are replaced with *.
- Do not add new words or explanations.
- Replace each sensitive word with exactly one *.
- Preserve the original line breaks, except that empty lines may be removed.
- Carefully check that no personal identifiers remain visible.
- Do not anonymise ordinary medical terminology merely because it
  appears in a medical document.
  
  CRITICAL EXCEPTIONS:
- Keep the document title unchanged.
- Keep the admission date unchanged.
- Keep the reference number ADM-2025-04-15-089 unchanged.
- Preserve all section headings.
- Do not anonymise information simply because it contains numbers.
- Only anonymise information that is genuinely sensitive or identifies
  an individual.

DOCUMENT:
{text}
"""
body = {
    "contents": [
        {
            "parts": [
                {"text": prompt}
            ]
        }
    ],
    "generationConfig": {
    "temperature": 0.0,
    "thinkingConfig": {
        "thinkingBudget": 0
    }
},
}

# Send our request to Gemini
response = requests.post(
    api_url,
    headers={"x-goog-api-key": api_key},
    json=body,
    timeout=180,
)

if response.status_code != 200:
    print("Google's error:", response.text)
response.raise_for_status()


# Display Gemini's answer
result = response.json()
# Get Gemini's anonymised document
anonymised_text = result["candidates"][0]["content"]["parts"][0]["text"]

# Find our submission folder
submission_dir = PROJECT_DIR / "submission"

# Save the exact prompt sent to Gemini
(submission_dir / "prompt.txt").write_text(
    prompt,
    encoding="utf-8"
)

# Save Gemini's anonymised document
(submission_dir / "submission.txt").write_text(
    anonymised_text,
    encoding="utf-8"
)

print("SUCCESS! Both files have been saved!")