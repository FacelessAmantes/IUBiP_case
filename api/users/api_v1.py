from fastapi import APIRouter
from users.models import User


router = APIRouter(prefix='/users')


@router.post('/registration')
def reg_user(user:User):
    # тут логика добавления логики
    status = True
    element_id = 0
    if status:
        response = {'status':True, 'id':element_id}
    else:
        response = {"status":False, 'error_code':1, 'error_message':''}

    return response

@router.delete('/delete')
def delete_user(login:str):
    pass
# Тут логика удаления юзера
