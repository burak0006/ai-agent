from typing import Optional
from langchain.docstore.document import Document

def make_doc(
    text: str,
    company: Optional[str] = None,
    source: Optional[str] = None,
    period: Optional[str] = None,
    date: Optional[str] = None,
) -> Document:
    """Utility to build a Document with company + optional source metadata."""
    metadata = {}
    if company:
        metadata["company"] = company
    if source:
        metadata["source"] = source
    if period:
        metadata["period"] = period
    if date:
        metadata["date"] = date
    print(metadata)
    return Document(page_content=text, metadata=metadata)