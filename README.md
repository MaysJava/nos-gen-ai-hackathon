## MK Team
The *-Files: Intelligent Document Anonymisation

JunctionX Lisbon 2026 | NOS Generative AI Challenge

Protecting identities. Preserving information.

## Overview

Team Untrace is an AI-powered document anonymisation solution developed for the NOS challenge at JunctionX Lisbon 2026.

Our system uses Google Gemini, Python, and PyMuPDF to identify and mask personally identifiable information in a medical document while preserving its structure, readability, and clinical context.

Instead of simply deleting sensitive information or replacing entire sentences, our solution uses context-aware prompt engineering to replace each sensitive word with a single asterisk (*).

## Our goal is simple:
Make sensitive documents safer to share without losing the information that makes them useful.

## The Challenge
Organisations often work with documents containing personal, financial, medical, and other sensitive information.

Traditional anonymisation approaches based on fixed patterns can identify obvious information such as email addresses or telephone numbers, but they may struggle with contextual information such as names, relationships, and other identifying details.

The NOS challenge asks teams to develop an LLM-based solution that:
- Detects sensitive and personally identifiable information.
- Replaces sensitive words and numbers with *.
- Preserves non-sensitive information and document meaning.
- Maintains the original document's structure and formatting, with empty lines removed.
- Produces an anonymised output and the exact prompt used to generate it.

## Our Solution
Team Untrace combines LLM-based anonymisation with automated validation.

Our approach has five stages:
1. Document extraction
The system reads the original PDF using PyMuPDF and extracts its text.

2. Context-aware prompt engineering
A carefully designed prompt instructs Gemini to distinguish sensitive identifiers from information that should remain visible, while preserving the original text structure.

3. AI-powered anonymisation
Google Gemini processes the extracted document and replaces identified sensitive words with asterisks *.

4. Output formatting
The program removes empty lines while preserving the order and content of non-empty lines.

5. Automated validation
A separate Python checker examines the generated output for common anonymisation and formatting problems.

## Technology Stack
Python: Main programming language

Google Gemini API: Context-aware sensitive information detection and masking.

PyMuPDF: PDF text extraction

Requests: Communication with the Gemini API

python-dotenv: Loading the API key from a local environment file

flake8: Python code-quality checking

Git and GitHub: Version control, collaboration, and submission

## How It Works
Original Medical PDF
        |
        v
  PyMuPDF Extraction
        |
        v
  Structured AI Prompt
        |
        v
   Google Gemini API
        |
        v
  Anonymised Response
        |
        v
  Empty-Line Removal
        |
        v
  submission.txt
        |
        v
  Validation Checker

## Example
    Original:
    Nome: Maria Conceição Oliveira Santos
    Telefone: +351 912 345 678
    Email: maria.santos@emailpessoal.pt

    Anonymised:
    Nome: * * * *
    Telefone: * * * *
    Email: *

The model masks sensitive words while retaining labels, punctuation, and the surrounding document structure.
 
## Project Structure
nos-gen-ai-hackathon/
│
├── raw_data/
│   └── document_to_anonymize.pdf
│
├── submission/
│   ├── anonymize.py
│   ├── check_output.py
│   ├── prompt.txt
│   └── submission.txt
│
├── tutorials/
│
├── .gitignore
└── README.md

## Key files
    - anonymize.py — extracts the PDF text, builds the prompt, calls Gemini, and saves the results.
    - check_output.py — validates the generated output.
    - prompt.txt — stores the prompt sent to the model.
    submission.txt — contains the anonymised text evaluated by the NOS challenge.
    - document_to_anonymize.pdf — original challenge document.
 
## Getting Started
Prerequisites
You will need:
    - Python 3 installed.
    - A Google Gemini API key.
    - Git, if cloning the repository.
    - An internet connection to access the Gemini API.

1. Clone the repository
git clone https://github.com/MaysJava/nos-gen-ai-hackathon.git
cd nos-gen-ai-hackathon
git switch team-untrace

2. Create a virtual environment
On macOS or Linux:
python3 -m venv .venv
source .venv/bin/activate

On Windows:
python -m venv .venv
.venv\Scripts\activate

3. Install dependencies
python -m pip install pymupdf requests python-dotenv flake8

4. Configure the API key
Create a file called .env in the project root:
GEMINI_API_KEY=your_api_key_here
Replace your_api_key_here with your own Gemini API key.

Security: Never upload your .env file or share your API key publicly. The environment file should remain excluded from Git using .gitignore.

5. Run the anonymisation
From the project root:
python submission/anonymize.py
The program reads the source PDF, sends the anonymisation prompt to Gemini, and saves the resulting files under submission/.

6. Validate the output
python submission/check_output.py

7. Check code quality
python -m flake8 submission/anonymize.py submission/check_output.py
No terminal output indicates that flake8 found no style violations in these files.

## Validation and Quality Assurance
We developed a dedicated validation script rather than relying solely on the model's response.
Our checker currently verifies:
    - The anonymised output is not empty.
    - Required document headings remain present.
    - Obvious email addresses are not exposed.
    - Common Portuguese telephone-number patterns are not exposed.
    - Obvious credit-card patterns are not exposed.
    - Selected non-sensitive fields remain unchanged.
    - Empty lines have been removed.
    - The original and anonymised documents contain the same number of non-empty lines.
    - Lines containing changed words are flagged for manual review.

## Current test results
    - During local testing, the system successfully:
    - Produced an anonymised document using Gemini.
    - Preserved 60 non-empty lines from the source document.
    - Removed empty lines.
    - Preserved important headings, the admission date, and the document reference.
    - Passed the implemented pattern-based validation checks.
    - Passed flake8 checks.

Validation limitations: These checks do not guarantee that every sensitive identifier has been masked correctly. Changed-word review flags may include correct anonymisations.
 
## Reliability and Error Handling
External AI APIs may occasionally become unavailable due to temporary server demand or connection problems.

To improve reliability, the system includes an automatic retry mechanism for temporary API failures, including rate-limit and server-side errors.

The implementation retries eligible failures up to three attempts, with short delays between attempts.

This helps the program recover from temporary service interruptions without requiring immediate manual intervention.

## Engineering Decisions
Why an LLM instead of only regular expressions?

    Regular expressions are useful for recognising fixed patterns such as email addresses and telephone numbers.

    However, sensitive information is not always identifiable through its format alone.

    An LLM can consider the surrounding text and identify contextual information, such as a person's name in a medical narrative.

    We therefore use Gemini for anonymisation and pattern-based checks as an additional validation layer.

Why preserve medical context?
    Removing entire sentences or masking every medical term can make a document difficult to understand.

    Our prompt aims to preserve the clinical meaning while anonymising identifying details.

Why save the exact prompt?
    Prompt engineering is a core component of the NOS challenge.

    Saving the prompt provides transparency, reproducibility, and a way to evaluate how the model was instructed to perform anonymisation.

Why use a separate validation script?
    Separating generation from validation makes the solution easier to test, explain, maintain, and improve.

    It also allows us to detect formatting issues without repeatedly calling the Gemini API.

## Limitations and Future Improvements
This is a hackathon prototype, not a certified production-grade medical privacy solution.

Potential future improvements include:
    - More advanced detection of indirect identifiers.
    - Automated comparison of preserved non-sensitive content.
    - Additional tests for over-anonymisation and missed identifiers.
    - Support for more document formats and languages.
    - A human review interface for ambiguous cases.
    - More comprehensive handling of API availability and rate limits.
 
## Team Collaboration
MK team was developed collaboratively during JunctionX Lisbon 2026.

Our workflow uses GitHub branches, commits, and integration of team contributions to keep the project organised and maintain a transparent development history.

The repository history documents our development process, including improvements to the anonymisation pipeline, validation, reliability, and documentation.

## Hackathon Submission
Challenge: The -Files: Call for Anonymizing Prompts
Organiser: NOS
Event: JunctionX Lisbon 2026
Team: MK

The challenge submission includes:
    - submission/submission.txt
    - submission/prompt.txt
    - submission/anonymize.py
    - Supporting materials include the validation script and project documentation.

The final submission is made through a pull request to the original NOS hackathon repository and registered on the JunctionX platform.
 
## MK Team
Protecting identities. Preserving information.
Because useful information shouldn't have to come at the cost of privacy.
