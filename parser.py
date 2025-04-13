import requests


urls = \
[
    'https://market.yandex.ru/?ysclid=m9d9bhb5mx799401654&wprid=1744404360399560-470754862746750413-balancer-l7leveler-kubr-yp-sas-198-BAL&utm_source_service=web&src_pof=703&icookie=5FNtaupA1ZNnV6WJCvR8x6epqlZr%2F%2BnfqJF7ph0L4ZLYeChYG%2B%2FzqU8zpKx%2FKUM9ztmjBz0%2FJZJPQJfZZmz%2BvxTpiIY%3D&baobab_event_id=m9d9bhb5mx',
    'https://market.yandex.ru/product--maska-sfericheskaia-polnolitsevaia-6800-panoramnaia-s-filtrami/1909972184?sku=102203133644&uniqueId=12707986&do-waremd5=AQWmagIiuUGWV4CFjuBXwg&sponsored=1&cpc=yT4SBUOzqcmPpY9DZIJTj93tgS_GXjYeQy6V4vuCJNOiZXpJa7LbfZh-VXYc2aqK10y0Ps0stt-VzOPIj3fz-J_UdPYbEZ9F98yRCy04JY-R1BiCOmBonuJuR8G8r5cQqAzVBoTBilJK27UaSyLlZs3cbqkGV4FziNb46Jzq9VM4ql6Mvxt0OWOoL_Bj7z2Ky2EHB9Sl_S5AzqJ-knbWF0rw8YvoIvue79FIwzgzSiS3pC3BmIE3dTulZA4NIEtse_Yt3IiW_UpYXTNrkxmUNDxgzak3cI31wDVA25EHk_0npcR6UwnGjKFoEH_FGQhWAhM4L8qmiYLsa80qUcSPDQwcp7KkZ3CGURx8BJz4_3-_SK2WHWPIxMWnSXdBwBJX9SQiPbtoETdqDYCFfCOyXTuexN9TOjjWZmS-0Tcp4w3bVc8gKZxUoQFnroKQ-EA_TVM25dNrk9wef3oCjSSyACj-zFHqRCkl94J3jMnF0g1WJjohOn7J6Jz3vpDZPup_5ZWce_ZFdC4%2C'
]

BASE_URL = "http://localhost:8000/" 
api_url = 'v1/prices/get_products'
# api_url = 'v1/auth/reg'


data = {'urls':urls, "user_id":''}
response = requests.request('get', url=BASE_URL + api_url, json =data)

print(response.json())
