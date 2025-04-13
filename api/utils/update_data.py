import asyncio
import threading
from sqlalchemy.orm import Session
from random import randint
import time
from prices_service.api import UrlPrice
from utils.Parser import Parser
from database.db import get_db

# Предполагается, что Parser и UrlPrice уже определены

async def data_update(db: Session):
    parser = Parser()

    try:
        await parser.open()
    except Exception as e:
        print(f"Error opening parser: {e}")
        return

    while True:
        results = db.query(UrlPrice).all()
        for url in set(item.url for item in results):
            try:
                html = await parser.get_page_content(url)
            except Exception as e:
                print(f"Error fetching page content for {url}: {e}")
                continue

            floorPrice = randint(1000, 10000)
            db.add(UrlPrice(url=url, floorPrice=floorPrice, maxPrice=randint(floorPrice, floorPrice + 10000), timestamp=time.time()))
            db.commit()

        await asyncio.sleep(3600)  # Используем асинхронный sleep

    try:
        await parser.close()
    except Exception as e:
        print(f"Error closing parser: {e}")

def run_data_update():
    db = next(get_db())  # Получаем сессию
    try:
        asyncio.run(data_update(db))
    finally:
        db.close()

def start_data_update():
    thread = threading.Thread(target=run_data_update)
    thread.start()