## MK Team — Anonymisation Solution
## Overview
MK is a Python-based document anonymisation solution developed for the NOS Hackathon challenge.

The system uses Google's Gemini large language model (LLM) to identify and mask sensitive information in a Portuguese medical document while aiming to preserve the original meaning, non-sensitive information and document structure.

## How Our Solution Works
Our solution follows five main steps:
    1. Extract the document text
        The Python script reads raw_data/document_to_anonymize.pdf using PyMuPDF and extracts its text.

    2. Prepare the anonymisation prompt
        The extracted text is combined with a detailed prompt that instructs Gemini to:
            - Identify and anonymise sensitive personal information.
            - Replace each sensitive word with a single *.
            - Preserve non-sensitive information, punctuation and the original meaning.
            - Maintain the document's line structure.

    3. Send the request to Gemini
        The script sends the prompt to the Gemini API and receives an anonymised version of the document.

        The API key is loaded from a local .env file rather than being included directly in the source code.

    4. Save the required outputs
        The program writes two files:
            - submission/prompt.txt — the exact prompt used for the API request.
            - submission/submission.txt — the generated anonymised document, with empty lines removed.

    5. Validate the result
        The project includes two forms of automated checking:

        - `check_output.py` performs the project's output-validation checks.
        - `test_validation.py` contains unit tests that check for common formatting issues, required headings, and email or phone-number patterns.

        These checks help identify potential problems, but manual review may still be needed because no automated checker can guarantee complete anonymisation.

## Technologies Used
Python: Main programming language
PyMuPDF:Extract text from the PDF
Google Gemini API: Context-aware text anonymisation
Requests: Communicate with the Gemini API
python-dotenv: Load the API key securely
flake8: Check Python code quality
Git and GitHub: Version control and team collaboration

## How to Run
From the project root, install the required Python packages:

python -m pip install pymupdf requests python-dotenv flake8

Create a .env file in the project root containing:

GEMINI_API_KEY=your_api_key_here

Run the anonymisation program:

python submission/anonymize.py

Then validate the generated document:

python submission/check_output.py

To check Python code style:

python -m flake8 submission/anonymize.py submission/check_output.py

## Dashboard

A browser-based dashboard is included at `dashboard/index.html` in the project root.

The dashboard is a separate component from the anonymisation script and validation tools. See the main project README for the dashboard's location and usage instructions.

The core anonymisation process can be run independently using `python submission/anonymize.py`.

## Validation Strategy
    - Our validation script checks that:
    - The anonymised document exists and is not empty.
    - Important document headings are preserved.
    - Common email, telephone and payment-card patterns are not exposed.
    - Selected non-sensitive fields remain unchanged.
    - Empty lines have been removed.
    - The number of non-empty lines matches the original document.
    - Modified lines are highlighted for manual review.

During our latest local test, both the original and anonymised documents contained 60 non-empty lines, and the automated checks reported no failures.

The checker also flagged 24 lines for review. These are not necessarily errors; they may include correctly anonymised content.

Running the Unit Tests

    From the project root, run:

    Windows:
    python -m unittest discover -s submission -p "test_validation.py" -v
    

    macOS or Linux:
    python3 -m unittest discover -s submission -p "test_validation.py" -v

    The tests read `submission/submission.txt` and check that it is not empty, required headings are present, email addresses and common Portuguese mobile phone numbers matching the test patterns are absent, and empty lines have been removed.

    These unit tests complement `check_output.py` by checking a small set of expected conditions. They do not modify `anonymize.py`, `prompt.txt`, or `submission.txt`, and passing them does not guarantee that all sensitive information has been anonymised correctly.

## Reliability Improvements
The Gemini API can occasionally return temporary errors due to high demand or service availability.

To make our solution more reliable, we added an automatic retry mechanism for selected temporary API errors.

The program makes up to three attempts before reporting a failure.

## Design Decisions
Why use an LLM?
    Sensitive information is not always recognisable through simple patterns. An LLM can use the surrounding context to identify information that may require anonymisation.

Why preserve document structure?
    The goal is to protect identities without making the medical document difficult to read or understand.

Why add automated validation?
    AI-generated results may contain mistakes. Automated checks help identify common privacy and formatting issues before submission.

Why use separate scripts?
    Keeping anonymisation and validation separate makes the system easier to test, understand and maintain.

## Limitations
Our system is a working prototype, not a guarantee of complete privacy protection.

The validation checks cannot detect every possible type of sensitive information, and ambiguous information may require human review.

The quality of the final output depends on the model's interpretation of the prompt and the document.

## Future Improvements
With additional development time, we would explore:
    - More comprehensive detection of sensitive information.
    - A stronger evaluation system using labelled test documents.
    - More advanced detection of unnecessary anonymisation.
    - Support for additional document types.
    - A simple user interface for uploading and reviewing documents.

MK Team— Protecting identities. Preserving information.