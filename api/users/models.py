from pydantic import BaseModel 
from sqlalchemy import Column, Integer, String
from db.db import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key= True, unique=True)
    login = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=True, index=True)



class UserCreate(BaseModel):
    login: str
    email: str  # Используем EmailStr для валидации email
    password: str  # Минимальная длина пароля 8 символов
