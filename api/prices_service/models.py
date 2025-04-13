from sqlalchemy.types import Integer, String, TupleType, Boolean, Float
from sqlalchemy import Column
from pydantic import BaseModel, constr
from database.db import Base, engine
from typing import List


class StartParsingRequest(BaseModel):

    email: str
    urls: List[str]
 
class UserLinks(Base):

    __tablename__ = 'userLinks'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, index=True, unique=False)
    urls = Column(String)
    is_check = Column(Boolean)


class PriceItem(BaseModel):

    url: str
    floorPrice: float
    maxPrice: float
    timestamp: float


class PriceContainer(BaseModel):
    
    status: bool
    content: List[PriceItem]
    totalItems: int


class UrlPrice(Base):

    __tablename__ = 'urlPrice'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    url = Column(String, index=True, unique=False)
    floorPrice = Column(Float)
    maxPrice = Column(Float)
    timestamp =  Column(Float)


Base.metadata.create_all(engine)