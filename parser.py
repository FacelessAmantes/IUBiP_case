import asyncio
import time 
from datetime import date



        




# asyncio.run(main())

import requests


urls = {'urls': ['https://market.yandex.ru/product--maska-sfericheskaia-polnolitsevaia-6800-panoramnaia-s-filtrami/1909972184?sku=102203133644&uniqueId=12707986&do-waremd5=AQWmagIiuUGWV4CFjuBXwg&sponsored=1&cpc=yT4SBUOzqcmPpY9DZIJTj93tgS_GXjYeQy6V4vuCJNOiZXpJa7LbfZh-VXYc2aqK10y0Ps0stt-VzOPIj3fz-J_UdPYbEZ9F98yRCy04JY-R1BiCOmBonuJuR8G8r5cQqAzVBoTBilJK27UaSyLlZs3cbqkGV4FziNb46Jzq9VM4ql6Mvxt0OWOoL_Bj7z2Ky2EHB9Sl_S5AzqJ-knbWF0rw8YvoIvue79FIwzgzSiS3pC3BmIE3dTulZA4NIEtse_Yt3IiW_UpYXTNrkxmUNDxgzak3cI31wDVA25EHk_0npcR6UwnGjKFoEH_FGQhWAhM4L8qmiYLsa80qUcSPDQwcp7KkZ3CGURx8BJz4_3-_SK2WHWPIxMWnSXdBwBJX9SQiPbtoETdqDYCFfCOyXTuexN9TOjjWZmS-0Tcp4w3bVc8gKZxUoQFnroKQ-EA_TVM25dNrk9wef3oCjSSyACj-zFHqRCkl94J3jMnF0g1WJjohOn7J6Jz3vpDZPup_5ZWce_ZFdC4%2C']}


url = 'http://localhost:8000/markets_prices/get_prices_v2'


response = requests.request('POST',url=url, json =urls)

print(response.json())

# import sqlalchemy
# from sqlalchemy.orm import sessionmaker, Session

# db_params = {"host":"64.188.97.135", 'user':"bober", 'password':'0000', 'table':'users'}


# DATABASE_URL = f"postgresql://{db_params.get('user')}:{db_params.get('password')}@{db_params.get('host')}/{db_params.get('table')}"  # Замените на вашу строку подключения
# engine = sqlalchemy.create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# db = SessionLocal()

# print(db.query().all())

