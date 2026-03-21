"""Extracts text content from uploaded PDF files."""

from typing import Any

from PyPDF2 import PdfReader


def read_pdf(file: Any) -> str:
    """Returns all text extracted from a PDF file object, pages joined by newlines."""
    reader = PdfReader(file)
    extracted_text = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)
    return "\n".join(extracted_text)
