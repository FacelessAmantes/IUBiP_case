from fastapi import FastAPI
from prices_service.api import router
from auth_service.api import auth_router
from fastapi.middleware.cors import CORSMiddleware

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