from fastapi import APIRouter, Depends, HTTPException
from users.models import User, UserCreate
from sqlalchemy.orm import Session
from db.db import get_db 
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
router = APIRouter(prefix='/users')


@router.post('/registration')
def reg_user(user:UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(login=user.login, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return JSONResponse()
    except IntegrityError as e:
        db.rollback()  # Откат транзакции в случае ошибки
        raise HTTPException(status_code=400, detail="User  with this login or email already exists.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/delete')
def delete_user(login:str):
    pass
# Тут логика удаления юзера
