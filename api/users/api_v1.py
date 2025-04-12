from fastapi import APIRouter, Depends, HTTPException
from users.models import User, UserCreate
from sqlalchemy.orm import Session
from db.db import get_db 
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
router = APIRouter(prefix='/users')


@router.post('/registration')
def reg_user(payload:UserCreate, db: Session = Depends(get_db)):
    try:
        # Создание нового пользователя
        db_user = User(login=payload.login, email=payload.email, password=payload.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)  # Обновление объекта db_user с данными из базы данных

        return {"status": "success", "user_id": db_user.id}  # Возвращаем ID нового пользователя
    except IntegrityError as e:
        db.rollback()  # Откат транзакции в случае ошибки
        return {'error':e}
        raise HTTPException(status_code=400, detail="User  with this login or email already exists.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))

@router.delete('/delete')
def delete_user(login:str):
    pass
# Тут логика удаления юзера
