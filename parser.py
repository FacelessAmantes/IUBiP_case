import asyncio
import nodriver as uc
import time 
from datetime import date

async def main():
    url = 'https://www.ozon.ru/product/holodilnik-s-nizhney-morozilnoy-kameroy-hyundai-cc30031-obem-296l-klass-a-uroven-shuma-40-db-1771312553/?campaignId=535'
    browser = await uc.start()
    page = await browser.get(url=url)


    time.sleep(4)

    sales_element = await page.query_selector('[data-widget="webPrice"]')

    print(type(sales_element))
    time.sleep(100)



# asyncio.run(main())

import requests

url = 'http://localhost:8000/markets_prices/history'

data = {'ids':[213, 12, 232, 121], 'date_from': '2024.02.01', 'date_to': '2024.02.01'}

response = requests.request('GET',url=url, json=data)

print(response.json())