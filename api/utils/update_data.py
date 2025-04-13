import asyncio
import threading
from sqlalchemy.orm import Session
from random import randint
import time
from prices_service.api import UrlPrice
from utils.Parser import Parser
from database.db import get_db
from utils.price_script import parse

# Предполагается, что Parser и UrlPrice уже определены

async def data_update(db: Session):
    driver = Parser()
    await driver.open()

    while True:
        results = db.query(UrlPrice).all()
        for url in set(item.url for item in results):
            try:
                html = await driver.get_page_content(url)
                prices = parse(url, html=html)
            except Exception as e:
                print(f"Error fetching page content for {url}: {e}")
                continue

            floorPrice = randint(1000, 10000)
            print(prices)
            db.add(UrlPrice(url=url, floorPrice=prices[0], maxPrice = prices[1], timestamp=time.time()))
            db.commit()

        await asyncio.sleep(3600)  # Используем асинхронный sleep

 

def run_data_update():
    db = next(get_db())  # Получаем сессию
    try:
        asyncio.run(data_update(db))  # Run the async function

    finally:
        db.close()

