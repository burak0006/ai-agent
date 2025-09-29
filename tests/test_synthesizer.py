from src.nine_fin_agent.snythesizer.info import synthesize_company_info
from src.nine_fin_agent.schema import Company

def test_synthesize_company_info():
    company = Company(
        company_id=1,
        company="Tronox",
        currency="USDm",
        periods=[],
        key_financials={"url": "/company_id/1/key_financials", "rows": []},
        cash_flow_and_leverage={"url": "/company_id/1/cash_flow_and_leverage", "rows": []},
        cap_table={"as_of": "2024-12-31", "url": "/company_id/1/cap_table", "rows": []}
    )
    docs = synthesize_company_info(company)
    assert any("Tronox" in d.page_content for d in docs)
