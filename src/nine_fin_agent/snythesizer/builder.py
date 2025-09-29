from langchain.docstore.document import Document
from typing import List

from src.nine_fin_agent.schema import Company
from src.nine_fin_agent.snythesizer.info import (
    synthesize_company_info,
    synthesize_periods,
)
from src.nine_fin_agent.snythesizer.metrics import synthesize_metrics
from src.nine_fin_agent.snythesizer.cap import synthesize_cap_table


def synthesize_company_sentences(company: Company) -> List[Document]:
    """Document Extraction"""
    docs: List[Document] = []
    docs.extend(synthesize_company_info(company))
    docs.extend(synthesize_periods(company))
    docs.extend(synthesize_metrics(company))
    docs.extend(synthesize_cap_table(company))
    return docs


def synthesize_documents(data: dict) -> List[Document]:
    """Synthesize documents"""
    docs: List[Document] = []
    for company in data["company_financials"]:
        company_model = Company(**company)
        docs.extend(synthesize_company_sentences(company_model))
    return docs
