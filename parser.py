import asyncio
import time 
from datetime import date



        




# asyncio.run(main())

import requests




# url = 'http://localhost:8000/markets_prices/history'

# data = {'ids':[322, 3212, 2311], 'date_from':'24-06-2006', 'date_to': '25-06-2006'}
# response = requests.request('GET',url=url, json =data)


url = 'http://localhost:8000/users/registration'

data = {'login':'Kisnge2r', 'email':'email322@gmail.com', 'password':'321231e323212'}
response = requests.request('POST', url=url, json =data)

print(response.content)

# import sqlalchemy
# from sqlalchemy.orm import sessionmaker, Session

# db_params = {"host":"64.188.97.135", 'user':"bober", 'password':'0000', 'table':'users'}


# DATABASE_URL = f"postgresql://{db_params.get('user')}:{db_params.get('password')}@{db_params.get('host')}/{db_params.get('table')}"  # Замените на вашу строку подключения
# engine = sqlalchemy.create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# db = SessionLocal()

# print(db.query().all())

