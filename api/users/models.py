from pydantic import BaseModel, EmailStr, constr
from pydantic.types import SecretStr, StringConstraints 
from sqlalchemy import Column, Integer, String
from db.db import Base


class User(Base):

    __tablename__ = 'users'

    login = Column(String)
    email = Column(String, primary_key= True, unique=True)
    password = Column(String)



class UserCreate(BaseModel):
    login: str
    email: EmailStr  # Используем EmailStr для валидации email
    password: constr(min_length=8) # Минимальная длина пароля 8 символов
