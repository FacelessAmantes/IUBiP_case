from pydantic import BaseModel 


class User(BaseModel):

    id:int
    login:str
    email:str
    password:str
    