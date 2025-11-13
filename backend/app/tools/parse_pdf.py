from langchain.tools import tool
from pypdf import PdfReader

@tool 
def parse_pdf(path: str) -> str:
    """
    Purpose:
        Extract and return clean text from a PDF file.

    Use when:
        The user asks to read, summarize, analyze, or extract information 
        from a PDF document.

    Returns:
        A plain text string containing the extracted PDF text. 
        The text is concatenated from all pages.

    Notes:
        Only works with .pdf files. 
        Use this tool instead of trying to reason about PDF content manually.
    """
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        content = page.extract_text()
        if content:
            text += content + "\n"

    if not text.strip():
        return "No extractable text found in the PDF."

    return text[:5000]    