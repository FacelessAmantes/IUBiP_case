from pydantic import BaseModel
from datetime import date

class HistoryRequest(BaseModel):
    ids:int|list[int]
    date_from: str
    date_to: str

class ContentItem(BaseModel):
    date: str
    id: int
    first_price: float
    second_price: float

class HistoryResponse(BaseModel):
    status: str
    content: list[ContentItem]

class PricesRequest(BaseModel):
    urls:list[str]