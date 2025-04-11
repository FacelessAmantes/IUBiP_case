from fastapi import FastAPI
from markets_prices.api_v1 import price_router
from users.api_v1 import router

app = FastAPI()
app.include_router(router=price_router)
app.include_router(router=router)

