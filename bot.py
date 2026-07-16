import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("BOT_TOKEN topilmadi!")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
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
        "/start - botni boshlash\n"
        "/donate - donat qilish"
    )


@dp.message(Command("donate"))
async def donate(message: Message):
    await message.answer(
        "💰 Donat qilish uchun summani yuboring.\n\n"
        "Masalan: 10 USDT"
    )


@dp.message()
async def echo(message: Message):
    await message.answer(
        "Xabaringiz qabul qilindi ✅"
    )


async def main():
    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
