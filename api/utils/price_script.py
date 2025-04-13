import re
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from datetime import datetime

# === Загрузка токена из .env ===
load_dotenv('api/.env')

api_token = os.getenv("REPLICATE_API_TOKEN")


def parse(url,html):

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
                    prices.append(price)
            if price >= 500:
                return prices


    def create_json(prices, url):
        # Получаем минимальную и максимальную цену для конкретной ссылки
        floor_price = min(prices) if len(prices) > 0 else 0
        max_price = max(prices) if len(prices) > 0 else 0

        # Получаем текущую метку времени в формате SQL
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Формируем JSON для конкретной ссылки
        result = {
                    "url": url,
                    "floorPrice": floor_price,
                    "maxPrice": max_price,
                    "timestamp": timestamp  # Используем метку времени SQL
                }

        return result


    # === Запуск ===
    data = [
        {
            "url": url,
            "html": html
        }
    ]

    all_results = []

    for item in data:

        # Извлекаем все цены из страницы
        prices = extract_prices(html)

        # Формируем JSON для конкретной ссылки
        result = create_json(prices, item['url'])
        all_results.append(result)

    
    return prices
    # Сохраняем в JSON файл
    with open("result_prices.json", "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)


# Выводим результат
