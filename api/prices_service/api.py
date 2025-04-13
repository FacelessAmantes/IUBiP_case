from fastapi import APIRouter, Depends, HTTPException
from prices_service.models import *
from sqlalchemy.orm import Session 
from database.db import get_db
from utils.Parser import Parser
from random import randint
import time

router = APIRouter(prefix='/v1/prices')


@router.post('/start_parsing', response_model=PriceContainer)
async def start_parsing(payload: StartParsingRequest, db:Session =  Depends(get_db)):
    parser = Parser()
    items = []
    items_to_bd = []
    user_links = UserLinks(email = payload.email ,urls = '^'.join(payload.urls), is_check = False)
    try:
        db.add(user_links)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    # await parser.open()ё
    for url in payload.urls:
        # await parser.get_page_content(url=url)
        floorPrice=randint(1000, 10000)
        items.append(PriceItem(url=url, floorPrice=floorPrice, maxPrice = randint(floorPrice, floorPrice +10000), timestamp=time.time()))
        items_to_bd.append(UrlPrice(url=url, floorPrice=floorPrice, maxPrice = randint(floorPrice, floorPrice +10000), timestamp=time.time()))

    else:
        db.add_all(items_to_bd)
        db.commit()
        return PriceContainer(status=True, content=items, totalItems=len(items))


@router.get('/get_products')
def get_products(payload: StartParsingRequest, db:Session = Depends(get_db)):
    result = db.query(UrlPrice).filter(UrlPrice.url.in_(payload.urls)).all()
    # Проверяем, были ли найдены продукты
    if not result:
        raise HTTPException(status_code=404, detail="No products found for the provided URLs")

    return result
    

    
@router.post('/get_last')
def get_products(email:str, db:Session = Depends(get_db)):
    result = db.query(UserLinks).filter(UserLinks.email ==email).all()
    # Проверяем, были ли найдены продукты
    if not result:
        raise HTTPException(status_code=404, detail="No products found for the provided URLs")

    return result