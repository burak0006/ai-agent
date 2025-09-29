from src.nine_fin_agent.retriever.vectorize import retrieve

def test_retrieve_run_returns_str():
    query = "Tronox Sales 2024"
    result = retrieve.run(query)  # This gives just serialized (str)
    assert isinstance(result, str)
    assert "Tronox" in result