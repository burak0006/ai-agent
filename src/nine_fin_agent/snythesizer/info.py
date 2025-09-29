from langchain.docstore.document import Document

from src.nine_fin_agent.snythesizer.base import make_doc
from src.nine_fin_agent.schema import Company


def synthesize_company_info(company: Company) -> list[Document]:
    """Primary Caompany information with Schema validation"""
    docs: list[Document] = []
    docs.append(make_doc(f"The company name is {company.company} with id {company.company_id}.",\
                         company = company.company))
    docs.append(make_doc(f"The reporting currency is {company.currency} for company {company.company}.",\
                         company = company.company))
    return docs


def synthesize_periods(company: Company) -> list[Document]:
    """Periods Extraction"""
    docs: list[Document] = []
    for p in company.periods:
        docs.append(make_doc(
            f"There is a financial report dated {p.date} with period {p.period} for {company.company}."
        ,company = company.company))
    return docs