from fastapi import APIRouter


router = APIRouter(prefix='/users')


@router.post('/registration')
def reg_user(email:str, login: str, password:str):
    status = True
    element_id = 0
    if status:
        response = {'status':True, 'id':element_id}
    else:
        response = {"status":False, 'error_code':1, 'error_message':''}

    return response

