from fastapi import APIRouter
from markets_prices.models import HistoryRequest, HistoryResponse, PricesRequest
from utils.Parser import Parser
import re

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
def get_history(payload:HistoryRequest):
    # Тут запрос к бд на получении данных по фильру
    date_from = payload.date_from
    date_to = payload.date_to
    ids = payload.ids
    query = "SELECT *" \
    "FROM {table}" \
    "WHERE id in {ids}" \
    "and date >= {date_from}" \
    "and date <= {date_to}" \

    return HistoryResponse(status='succesed', content=[])