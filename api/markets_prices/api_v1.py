from fastapi import APIRouter, Depends
from markets_prices.models import HistoryRequest, HistoryResponse, PricesRequest, ContentItemResponse
from utils.Parser import Parser
import re
from sqlalchemy.orm import Session
from db.db import get_db 
from sqlalchemy import text


price_router = APIRouter(prefix='/markets_prices')


@price_router.post('/get_prices_v1')
async def post_price(payload:PricesRequest):
    response = []
    
    for url in payload.urls:
        pattern = r'\b(www.ozon.ru|market.yandex.ru|www.wildberries.ru|www.onlinetrade.ru|cdek.shopping)\b'  # \b - границы слова

    # Поиск всех совпадений
        match_res = re.search(pattern,url)
        if match_res:
            match match_res.group().lower():  # Приводим к нижнему регистру для обработки
                case "www.ozon.ru":
                    response.append ("Найден URL: Ozon.")
                case "market.yandex.ru":
                    response.append("Найден URL: Яндекс.Маркет.")
                case "www.wildberries.ru":
                    response.append("Найден URL: Wildberries.")
                case "www.onlinetrade.ru":
                    response.append("Найден URL: OnlineTrade.")
                case "cdek.shopping":
                    response.append("Найден URL: CDEK Shopping.")
                case _:
                    response.append("Найден другой URL.")
    else:
        return {'status':True, "content":response}
    

@price_router.post('/get_prices_v2')
async def post_price(payload:PricesRequest):
    response = []
    parser = Parser()
    await parser.open()

    for url in payload.urls:
        try:
            response.append(await parser.get_page_content(url))    
        except Exception as e:
            await parser.close()
            return {'status':False, 'error':e}
    else:
        await parser.close()
        return {'status':True, "content":response}



    
@price_router.get('/history', response_model=HistoryResponse)
def get_history(payload:HistoryRequest, db: Session = Depends(get_db)):
    date_from = payload.date_from
    date_to = payload.date_to
    ids = payload.ids
    # Формирование SQL-запроса
    query = text(
        "SELECT * FROM items_history "
        "WHERE product IN :ids "
        "AND date >= :date_from "
        "AND date <= :date_to"
    )

    # Выполнение запроса
    result = db.execute(query, {
        "ids": tuple(ids) if isinstance(ids, list) else (ids,),
        "date_from": date_from,
        "date_to": date_to
    }).fetchall()

    # Преобразование результата в список Pydantic моделей
    content = [
        ContentItemResponse(
            product=row.product,
            date=row.date,
            first_price=row.first_price,
            second_price=row.second_price
        )
        for row in result
    ]

    return HistoryResponse(status='success', content=content)
