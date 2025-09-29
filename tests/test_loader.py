from src.nine_fin_agent.retriever.load_document import load_document
from langchain.docstore.document import Document
from pathlib import Path


def test_load_document():
    fixture_path = Path(__file__).parent / "fixture" / "sample_documents.json"
    docs = load_document(fixture_path)

    assert len(docs) == 2
    assert isinstance(docs[0], Document)

    tronox_doc = docs[0]
    assert "Tronox" in tronox_doc.page_content
    assert tronox_doc.metadata["company"] == "Tronox"
    assert tronox_doc.metadata["year"] == "2024"

    chemco_doc = docs[1]
    assert "Chemco Holdings" in chemco_doc.page_content
    assert chemco_doc.metadata["company"] == "Chemco Holdings"
    assert chemco_doc.metadata["metric"] == "EBITDA"
