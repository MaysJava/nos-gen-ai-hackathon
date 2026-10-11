
import re
import unittest
from pathlib import Path

OUTPUT = Path(__file__).parent / "submission.txt"


class TestAnonymisation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.text = OUTPUT.read_text(encoding="utf-8")

    def test_output_not_empty(self):
        self.assertTrue(self.text.strip())

    def test_no_email_addresses(self):
        pattern = r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"
        self.assertIsNone(re.search(pattern, self.text))

    def test_no_portuguese_phone_numbers(self):
        pattern = r"(?:\+351[\s-]?)?9\d{2}[\s-]?\d{3}[\s-]?\d{3}"
        self.assertIsNone(re.search(pattern, self.text))

    def test_headings_preserved(self):
        headings = [
            "Informações do Paciente:",
            "Histórico Médico:",
            "Informações Financeiras:",
            "Contatos de Emergência:",
        ]
        for heading in headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.text)

    def test_no_empty_lines(self):
        self.assertTrue(
            all(line.strip() for line in self.text.splitlines())
        )


if __name__ == "__main__":
    unittest.main()
