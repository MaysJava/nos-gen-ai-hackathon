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

print("\nChecks finished!")