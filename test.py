# import pandas as pd
# import random
# from datetime import datetime, timedelta

# # Задаем параметры
# num_rows = 100
# products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
# start_date = datetime(2023, 1, 1)
# end_date = datetime(2023, 12, 31)

# # Генерация синтетических данных
# data = {
#     'product': [random.choice(products) for _ in range(num_rows)],
#     'parsing_date': [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in range(num_rows)],
#     'first_price': [round(random.uniform(10.0, 100.0), 2) for _ in range(num_rows)],
#     'second_price': [round(random.uniform(10.0, 100.0), 2) for _ in range(num_rows)],
# }

# # Создание DataFrame
# df = pd.DataFrame(data)


# df.to_csv('test_data.csv')


import nodriver as uc
import asyncio

asyncio.run(uc.start(headless=True))