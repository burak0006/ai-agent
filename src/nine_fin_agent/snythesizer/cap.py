from langchain.docstore.document import Document
from dotenv import load_dotenv
from typing import List
import os

from src.nine_fin_agent.snythesizer.base import make_doc
from src.nine_fin_agent.schema import Company

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def synthesize_cap_table(company: Company) -> List[Document]:
    """Cap Table Validation and Extraction"""
    docs: List[Document] = []
    cap_url = f"{BASE_URL}/company_id/{company.company_id}/cap_table"
    as_of = company.cap_table.as_of

    for row in company.cap_table.rows:  # row is CapTableRow (Pydantic)
        sentence = (
            f"As of {as_of}, {company.company} had {row.name} "
            f"with amount {row.amount_usdm} USDm"
        )
        if row.maturity:
            sentence += f", maturity {row.maturity}"
        if row.security:
            sentence += f", security {row.security}"
        if row.rate:
            sentence += f", rate {row.rate}"
        if row.x_ebitda is not None:
            sentence += f", equivalent to {row.x_ebitda}x EBITDA"
        if row.percent_cap is not None:
            sentence += f", representing {row.percent_cap}% of capital structure"

        docs.append(make_doc(sentence + ".", company=company.company, source=cap_url))

    return docs
