import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
import asyncio
import asyncpg
import os
from dotenv import load_dotenv

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


async def get_active_users():
    conn = await asyncpg.connect(DB_DSN)
    rows = await conn.fetch("SELECT tg_id FROM public.mailing_list WHERE is_active = TRUE")
    await conn.close()
    return [row["tg_id"] for row in rows]


async def notify_active_users(message: str):
    active_users = await get_active_users()
    for user_id in active_users:
        try:
            await bot.send_message(chat_id=user_id, text=message)
        except Exception as e:
            logging.error(f"Ошибка при отправке пользователю {user_id}: {e}")


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    full_name = message.from_user.full_name

    logging.info(f"Пользователь {full_name} (tg_id={user_id}) нажал /start")

    conn = await asyncpg.connect(DB_DSN)
    # Выполняем запрос, чтобы получить пользователя
    user = await conn.fetchrow("SELECT * FROM mailing_list WHERE tg_id = $1", user_id)

    if user:
        logging.info(f"Данные пользователя из базы: {user}")
    else:
        logging.info(f"Пользователь с tg_id={user_id} не найден в базе данных.")

    if user is None:
        await message.answer("❌ Вас нет в системе, авторизуйтесь через сайт.")
    else:
        if not user["is_active"]:
            await conn.execute("UPDATE mailing_list SET is_active = TRUE WHERE tg_id = $1", user_id)
            logging.info(f"Пользователь {user_id} теперь подписан на уведомления.")
            await message.answer("✅ Вы подписаны на уведомления.")
        else:
            logging.info(f"Пользователь {user_id} уже подписан на уведомления.")
            await message.answer("✅ Вы уже подписаны на уведомления.")

    await conn.close()


@dp.message(Command("notify"))
async def notify_cmd(message: types.Message):
    await message.answer("Начинаю рассылку...")
    await notify_active_users("🔔 Уведомление для активных пользователей!")
    await message.answer("Рассылка завершена.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
