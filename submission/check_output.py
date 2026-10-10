import pymupdf
from pathlib import Path
import re

# Find the project folder
PROJECT_DIR = Path(__file__).resolve().parent.parent

# Read Gemini's anonymised document
output_path = PROJECT_DIR / "submission" / "submission.txt"
text = output_path.read_text(encoding="utf-8")

print("Checking anonymised document...\n")

# Check 1: Did Gemini return any text?
if text.strip():
    print("PASS: The output is not empty.")
else:
    print("FAIL: The output is empty.")

# Check 2: Are important headings preserved?
headings = [
    "Relatório de Admissão - Centro Médico Lisboa",
    "Informações do Paciente:",
    "Histórico Médico:",
    "Informações Financeiras:",
    "Contatos de Emergência:",
]

for heading in headings:
    if heading in text:
        print(f"PASS: Found heading: {heading}")
    else:
        print(f"FAIL: Missing heading: {heading}")

# Check 3: Did some obvious personal details remain?
sensitive_patterns = {
    "Email address": r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    "Portuguese phone number": r"\+351\s?\d[\d\s]{8,}",
    "Credit card number": r"\b(?:\d[ -]*?){13,19}\b",
}

for label, pattern in sensitive_patterns.items():
    if re.search(pattern, text):
        print(f"WARNING: Possible exposed {label}")
    else:
        print(f"PASS: No obvious {label} detected.")

    # Check 4: Important information must remain unchanged
required_lines = [
    "Data: 15 de abril de 2025",
    "Referência: ADM-2025-04-15-089",
    "Sexo: Feminino",
]

for line in required_lines:
    if line in text.splitlines():
        print(f"PASS: Preserved original line: {line}")
    else:
        print(f"FAIL: Original line was changed or removed: {line}")

# Check 5: Detect empty lines
empty_line_numbers = [
    number
    for number, line in enumerate(text.splitlines(), start=1)
    if not line.strip()
]

if empty_line_numbers:
    print(
        "FAIL: Empty lines found at line numbers:",
        empty_line_numbers
    )
else:
    print("PASS: No empty lines found.")

# Check 6: Compare line counts with the original PDF

pdf_path = PROJECT_DIR / "raw_data" / "document_to_anonymize.pdf"

with pymupdf.open(pdf_path) as document:
    original_text = "\n".join(
        page.get_text(sort=True) for page in document
    )

original_lines = [
    line for line in original_text.splitlines() if line.strip()
]

output_lines = [
    line for line in text.splitlines() if line.strip()
]

if len(original_lines) == len(output_lines):
    print(f"PASS: Both documents contain {len(output_lines)} non-empty lines.")
else:
    print(
        f"FAIL: Original has {len(original_lines)} lines, "
        f"but output has {len(output_lines)} lines."
    )

    # Check 7: Detect changes to non-sensitive words

for number, (original, anonymised) in enumerate(
    zip(original_lines, output_lines), start=1
):
    original_words = original.split()
    output_words = anonymised.split()

    original_visible = [
        word for word in original_words
        if word not in output_words
    ]

    if original_visible:
        print(
            f"REVIEW line {number}: "
            "Some original words were changed or anonymised."
        )

print("\nChecks finished!")
