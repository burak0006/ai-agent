from src.nine_fin_agent.schema import Company

def test_company_model_valid():
    data = {
        "company_id": 1,
        "company": "Tronox",
        "currency": "USDm",
        "periods": [{"date": "2024-12-31", "period": "Annual"}],
        "key_financials": {"url": "/company_id/1/key_financials", "rows": []},
        "cash_flow_and_leverage": {"url": "/company_id/1/cash_flow_and_leverage", "rows": []},
        "cap_table": {"as_of": "2024-12-31", "url": "/company_id/1/cap_table", "rows": []}
    }
    company = Company(**data)
    assert company.company == "Tronox"
    assert company.company_id == 1
