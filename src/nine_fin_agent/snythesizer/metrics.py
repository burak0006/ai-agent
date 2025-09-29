from langchain.docstore.document import Document
from dotenv import load_dotenv
from typing import List
import os

from src.nine_fin_agent.snythesizer.base import make_doc
from src.nine_fin_agent.schema import Company


load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def synthesize_metrics(company: Company) -> List[Document]:
    """Metrics Data Validation and Extraction"""
    docs: List[Document] = []

    for section_name in ["key_financials", "cash_flow_and_leverage"]:
        section = getattr(company, section_name)           # Financials object
        url = f"{BASE_URL}/company_id/{company.company_id}/{section_name}"

        for idx, period in enumerate(company.periods):     # List[Period]
            for row in section.rows:                       # List[MetricRow]
                val = row.values[idx]
                docs.append(make_doc(
                    (
                        f"In {period.date}, {company.company} reported "
                        f"{row.metric} of {val} {row.unit} "
                        f"(period: {period.period}) with url {url}"
                    ),
                    company = company.company,
                    period = period.period,
                    source = url,
                    date = period.date
                ))

    return docs
