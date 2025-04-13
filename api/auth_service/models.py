from sqlalchemy.types import Integer, String, TupleType, Boolean, Float
from sqlalchemy import Column
from pydantic import BaseModel, constr, EmailStr
from database.db import Base, engine

class UserRequest(BaseModel):

    email: EmailStr
    login: str
    password: str

class User(Base):

    __tablename__ = 'users'

    email = Column(String, primary_key=True, unique=True)
    login = Column(String)
    password = Column(String)
    
class UserCheckRequest(BaseModel):

    email: EmailStr
    password: str

Base.metadata.create_all(engine)