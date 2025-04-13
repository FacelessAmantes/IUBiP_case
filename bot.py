import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
import asyncio
import asyncpg
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")
DB_DSN = os.getenv("DATABASE_URL")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


async def notify_users_with_updated_links():
    conn = await asyncpg.connect(DB_DSN)

    # Берём последние 24 часа обновлений
    check_time = datetime.now() - timedelta(hours=24)

    # Все email, у кого были обновления ссылок
    rows = await conn.fetch("""
        SELECT DISTINCT ul.email, u.tg_id
        FROM user_links ul
        JOIN users u ON ul.email = u.email
        WHERE ul.timestamp > $1
    """, check_time)

    for row in rows:
        tg_id = row["tg_id"]
        email = row["email"]

        try:
            await bot.send_message(
                chat_id=tg_id,
                text="🔔 Обновилась информация по вашим отслеживаемым ссылкам!"
            )
            logging.info(f"Уведомление отправлено пользователю {tg_id} ({email})")
        except Exception as e:
            logging.error(f"Ошибка при отправке пользователю {tg_id}: {e}")

    await conn.close()


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("👋 Бот активен. Я пришлю уведомление, когда обновится информация по вашим ссылкам.")


@dp.message(Command("notify"))
async def notify_cmd(message: types.Message):
    await message.answer("🔄 Проверяю обновления по ссылкам...")
    await notify_users_with_updated_links()
    await message.answer("✅ Уведомления разосланы.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
