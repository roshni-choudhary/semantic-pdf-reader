"""
PDF Processor Module
Handles PDF text extraction, cleaning, and chunking for semantic search.
"""

from typing import List, Dict, Any
import re
from pypdf import PdfReader


def extract_text_from_pdf(pdf_file) -> List[Dict[str, Any]]:
    """
    Extracts text from an uploaded PDF file page by page.

    Args:
        pdf_file: File-like object (e.g., Streamlit UploadedFile or file path)

    Returns:
        List of dictionaries containing page_number and extracted text.
    """
    reader = PdfReader(pdf_file)
    extracted_pages = []

    for page_idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        cleaned_text = clean_text(text)
        if cleaned_text:
            extracted_pages.append({
                "page": page_idx + 1,
                "text": cleaned_text
            })

    return extracted_pages


def clean_text(text: str) -> str:
    """
    Cleans raw extracted text by normalizing whitespace.

    Args:
        text: Raw text string

    Returns:
        Cleaned text string
    """
    if not text:
        return ""
    # Replace multiple whitespaces/newlines with a single space
    cleaned = re.sub(r'\s+', ' ', text)
    return cleaned.strip()


def chunk_text(pages: List[Dict[str, Any]], chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Splits page text into smaller overlapping chunks for better semantic embedding granularity.

    Args:
        pages: List of page dictionaries with 'page' and 'text' keys.
        chunk_size: Approximate character length of each chunk.
        overlap: Character overlap between consecutive chunks.

    Returns:
        List of chunk dictionaries with 'chunk_id', 'page', and 'text'.
    """
    chunks = []
    chunk_id = 0

    for page in pages:
        page_num = page["page"]
        text = page["text"]

        if len(text) <= chunk_size:
            chunks.append({
                "chunk_id": chunk_id,
                "page": page_num,
                "text": text
            })
            chunk_id += 1
            continue

        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_str = text[start:end]

            # Try to break cleanly at sentence or word boundary if not at end of text
            if end < len(text):
                last_space = chunk_str.rfind(' ')
                if last_space > chunk_size // 2:
                    end = start + last_space
                    chunk_str = text[start:end]

            chunk_str = chunk_str.strip()
            if chunk_str:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_num,
                    "text": chunk_str
                })
                chunk_id += 1

            start += (chunk_size - overlap)

    return chunks
