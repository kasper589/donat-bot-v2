import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

import database as db

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await db.add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🎮 Donat botga xush kelibsiz!\n\n"
        "Buyruqlar:\n"
        "/donate - donat qilish\n"
        "/help - yordam"
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "ℹ️ Yordam:\n\n"
        "/start - boshlash\n"
        "/donate - donat qilish"
    )


@dp.message(Command("donate"))
async def donate(message: Message):
    await message.answer(
        "💰 Donat qilish uchun summani yuboring.\n\n"
        "Masalan: 10"
    )


@dp.message()
async def save_message(message: Message):
    await message.answer(
        "Xabaringiz qabul qilindi ✅"
    )


async def main():
    await db.init_db()

    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
