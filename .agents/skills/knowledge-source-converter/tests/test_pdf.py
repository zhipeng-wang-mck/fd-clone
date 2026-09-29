import sys
import tempfile
import unittest
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from pdf import pdf_to_markdown  # noqa: E402


def _write_pdf(path: Path, pages: list[list[str]], title: str = "") -> None:
    doc = pymupdf.open()
    for lines in pages:
        page = doc.new_page()
        page.insert_text((72, 72), "\n".join(lines))
    if title:
        doc.set_metadata({"title": title})
    doc.save(str(path))
    doc.close()


class PdfTitleTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.path = Path(self._tmp.name) / "doc.pdf"

    def tearDown(self):
        self._tmp.cleanup()

    def convert(self, pages, title=""):
        _write_pdf(self.path, pages, title)
        return pdf_to_markdown(self.path)

    def test_running_header_on_page_one_is_kept_once_as_title(self):
        header = "ACME - TOOLING STANDARD"
        md, notes = self.convert(
            [[header, "1. Scope", "CONFIDENTIAL", "Page 1"],
             [header, "2. Data", "CONFIDENTIAL", "Page 2"]]
        )
        self.assertEqual(md, f"# {header}\n\n1. Scope\n\n2. Data")
        self.assertIn(f"Kept running header '{header}' as the document title", notes)

    def test_repeated_banner_is_never_a_title(self):
        md, _ = self.convert([["CONFIDENTIAL", "Body one"], ["CONFIDENTIAL", "Body two"]])
        self.assertEqual(md, "Body one\n\nBody two")

    def test_metadata_title_used_when_no_running_header(self):
        md, notes = self.convert([["Body one"], ["Body two"]], title="Tooling Standard")
        self.assertEqual(md, "# Tooling Standard\n\nBody one\n\nBody two")
        self.assertIn("Used PDF metadata title 'Tooling Standard'", notes)

    def test_metadata_title_not_duplicated_when_it_opens_the_body(self):
        md, _ = self.convert([["Tooling Standard", "Body"]], title="Tooling Standard")
        self.assertEqual(md, "Tooling Standard\nBody")

    def test_no_title_is_invented(self):
        md, notes = self.convert([["Body one"], ["Body two"]])
        self.assertEqual(md, "Body one\n\nBody two")
        self.assertFalse(any("title" in n for n in notes))


if __name__ == "__main__":
    unittest.main()
