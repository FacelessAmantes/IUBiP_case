from fastapi import APIRouter
from markets_prices.models import HistoryRequest

price_router = APIRouter(prefix='/markets_prices')


@price_router.get('/get_prices')
def post_price():
    status = True
    element_id = 0
    if status:
        response = {'status':True, 'id':element_id}
    else:
        response = {"status":False, 'error_code':1, 'error_message':''}


    
@price_router.get('/history')
def get_history(payload:HistoryRequest):
    return payload