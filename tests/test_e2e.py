from pathlib import Path
import pytest

from src.nine_fin_agent.retriever.load_document import load_document, load_and_index
from src.nine_fin_agent.retriever.vectorize import retrieve


@pytest.mark.integration
def test_e2e_tronox_sales(tmp_path):
    fixture_path = Path(__file__).parent / "fixture" / "sample_documents.json"
    docs = load_document(fixture_path)

    vectorstore = load_and_index(docs)
    result = retrieve.run("Tronox Sales 2024")

    assert isinstance(result, str)
    assert "Tronox" in result
