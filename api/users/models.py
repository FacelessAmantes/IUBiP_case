from pydantic import BaseModel, EmailStr, constr
from pydantic.types import SecretStr, StringConstraints 
from sqlalchemy import Column, Integer, String
from db.db import Base
import 

class User(Base):

    __tablename__ = 'users'

    login = Column(String, nullable=False)  # Уникальный логин
    email = Column(String, unique=True, nullable=False, primary_key=True)  # Уникальный email
    password = Column(String, nullable=False)  # Пароль



class UserCreate(BaseModel):
    login: str
    email: EmailStr  # Используем EmailStr для валидации email
    password: constr(min_length=8) # Минимальная длина пароля 8 символов
