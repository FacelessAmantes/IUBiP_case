from fastapi import APIRouter, Depends, HTTPException, status
from auth_service.models import *
from sqlalchemy.orm import Session
from database.db import get_db

auth_router = APIRouter(prefix='/v1/auth')


@auth_router.post('/check_reg')
def auth(payload: UserCheckRequest, db: Session = Depends(get_db)):
    
    email = payload.email
    password = payload.password

    # Выполняем асинхронный запрос к базе данных
    user = db.query(User).filter_by(email=email).first()

    # Проверяем, существует ли пользователь и совпадает ли пароль
    if user and user.password == password:
        return {"status":True}  # Пароль верный

    # Если пользователь не найден или пароль неверный, выбрасываем исключение
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )

@auth_router.post('/reg')
def reg(payload: UserRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=payload.email).first()

    if user:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This user alreaady registered",
    )
    
    user = User(email = payload.email, password = payload.password, login = payload.login)
    db.add(user)
    db.commit()
    return {"status":True}
