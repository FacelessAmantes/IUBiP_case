from dotenv import load_dotenv
status = load_dotenv('api/.env')




from fastapi import FastAPI
from prices_service.api import router
from auth_service.api import auth_router
from fastapi.middleware.cors import CORSMiddleware
from utils.update_data import run_data_update
from utils.Parser import Parser
import os


app = FastAPI()
app.include_router(router=auth_router)
app.include_router(router=router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    
    run_data_update()


if __name__ == '__main__':
    import asyncio
    start()