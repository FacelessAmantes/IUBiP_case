import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime

# === Загрузка токена из .env ===
load_dotenv()

api_token = os.getenv("REPLICATE_API_TOKEN")


def normalize_price_text(text):
    return re.sub(r'[\s\u2009\u202f\u00a0]', '', text)


# Функция для извлечения цен
def extract_prices(html):
    soup = BeautifulSoup(html, 'html.parser')
    prices = []

    # Поиск по атрибутам
    attr_selectors = [
        {'attr': 'data-price'},
        {'attr': 'data-value'},
        {'attr': 'content', 'itemprop': 'price'},
        {'attr': 'value', 'class': re.compile(r'price|cost|product-price')}
    ]

    for selector in attr_selectors:
        attr = selector['attr']
        elements = []

        if 'itemprop' in selector:
            elements = soup.find_all(itemprop=selector['itemprop'])
        elif 'class' in selector:
            elements = soup.find_all(class_=selector['class'])
        else:
            elements = soup.find_all(attrs={attr: True})

        for el in elements:
            if attr in el.attrs:
                raw = normalize_price_text(el[attr])
                if raw.replace('.', '', 1).isdigit():
                    price = float(raw)
                    if price >= 1000:  # Убираем цены ниже 1000
                        prices.append(price)

    # Поиск цен в тексте страницы
    price_pattern = re.compile(
        r'(\d{1,3}(?:[ \u00a0\u2009\u202f]?\d{3})*(?:[\.,]\d{2})?)\s?(₽|руб|р|RUB|\$|€|EUR)',
        re.IGNORECASE
    )

    for tag in soup.find_all(text=True):
        if not tag.strip():
            continue
        matches = price_pattern.findall(tag)
        for match in matches:
            raw_price = normalize_price_text(match[0].replace(',', '.'))
            if raw_price.replace('.', '', 1).isdigit():
                price = float(raw_price)
                if price >= 1000:  # Убираем цены ниже 1000
                    prices.append(price)

    return prices


def create_json(prices, url):
    # Получаем минимальную и максимальную цену для конкретной ссылки
    floor_price = min(prices) if len(prices) > 0 else 0
    max_price = max(prices) if len(prices) > 0 else 0

    # Получаем текущую метку времени в формате SQL
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Формируем JSON для конкретной ссылки
    result = {
        "status": True,
        "content": [
            {
                "url": url,
                "floorPrice": floor_price,
                "maxPrice": max_price,
                "timestamp": timestamp  # Используем метку времени SQL
            }
        ],
        "totalItems": 1  # Каждая ссылка рассматривается отдельно
    }

    return result


# === Запуск ===
data = [
    {
        "url": "https://market.yandex.ru/card/maska-sfericheskaya-polnolitsevaya-6800-panoramnaya-s-filtrami/102203133644?do-waremd5=AQWmagIiuUGWV4CFjuBXwg&sponsored=1&cpc=yT4SBUOzqcmPpY9DZIJTj93tgS_GXjYeQy6V4vuCJNOiZXpJa7LbfZh-VXYc2aqK10y0Ps0stt-VzOPIj3fz-J_UdPYbEZ9F98yRCy04JY-R1BiCOmBonuJuR8G8r5cQqAzVBoTBilJK27UaSyLlZs3cbqkGV4FziNb46Jzq9VM4ql6Mvxt0OWOoL_Bj7z2Ky2EHB9Sl_S5AzqJ-knbWF0rw8YvoIvue79FIwzgzSiS3pC3BmIE3dTulZA4NIEtse_Yt3IiW_UpYXTNrkxmUNDxgzak3cI31wDVA25EHk_0npcR6UwnGjKFoEH_FGQhWAhM4L8qmiYLsa80qUcSPDQwcp7KkZ3CGURx8BJz4_3-_SK2WHWPIxMWnSXdBwBJX9SQiPbtoETdqDYCFfCOyXTuexN9TOjjWZmS-0Tcp4w3bVc8gKZxUoQFnroKQ-EA_TVM25dNrk9wef3oCjSSyACj-zFHqRCkl94J3jMnF0g1WJjohOn7J6Jz3vpDZPup_5ZWce_ZFdC4",
        "html": 'Маска_сферическая_полнолицевая_6800_панорамная_с_фильтрами_—_купить.html'
    },
    {
        "url": "https://www.onlinetrade.ru/catalogue/televizory-c181/xiaomi/televizor_xiaomi_mi_tv_a_43_2025_4k_ultra_hd_chernyy_l43ma_auru-4317073.html",
        "html": 'Телевизор_Xiaomi_Mi_TV_A_43_2025,_4K_Ultra_HD,_черный_L43MA_AURU.html'
    }
]

all_results = []

for item in data:
    with open(item['html'], 'r', encoding='utf-8') as file:
        html = file.read()

    # Извлекаем все цены из страницы
    prices = extract_prices(html)

    # Формируем JSON для конкретной ссылки
    result = create_json(prices, item['url'])
    all_results.append(result)

# Формируем итоговый JSON для всех ссылок
final_results = {
    "status": True,
    "content": [result["content"][0] for result in all_results],  # Берем только контент из каждого результата
    "totalItems": len(all_results)
}

# Сохраняем в JSON файл
with open("result_prices.json", "w", encoding="utf-8") as f:
    json.dump(final_results, f, ensure_ascii=False, indent=2)

# Выводим результат
print(json.dumps(final_results, ensure_ascii=False, indent=2))
