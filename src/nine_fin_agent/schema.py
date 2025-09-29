from pydantic import BaseModel
from typing import List, Optional


class Period(BaseModel):
    date: str
    period: str


class MetricRow(BaseModel):
    metric: str
    unit: str
    values: List[float]
    url: Optional[str] = None


class Financials(BaseModel):
    url: str
    rows: List[MetricRow]


class CapTableRow(BaseModel):
    name: str
    note: Optional[str] = None
    security: Optional[str] = None
    maturity: Optional[str] = None
    rate: Optional[str] = None
    amount_usdm: float
    x_ebitda: Optional[float] = None
    percent_cap: Optional[float] = None
    subtotal: Optional[bool] = False


class CapTable(BaseModel):
    as_of: str
    url: str
    rows: List[CapTableRow]


class Company(BaseModel):
    company_id: int
    company: str
    currency: str
    periods: List[Period]
    key_financials: Financials
    cash_flow_and_leverage: Financials
    cap_table: CapTable
