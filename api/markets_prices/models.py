from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date
from db.db import Base

class HistoryRequest(BaseModel):
    ids:int|list[int]
    date_from: str
    date_to: str

class ContentItem(Base):
    __tablename__ = "items_history"
    
    product = Column(String, primary_key=True)
    date = Column(Date)
    first_price = Column(Float)
    second_price = Column(Float)

class ContentItemResponse(BaseModel):
    product: str
    date: date
    first_price: float
    second_price: float


class HistoryResponse(BaseModel):
    status: str
    content: list[ContentItemResponse]

class PricesRequest(BaseModel):
    urls:list[str]