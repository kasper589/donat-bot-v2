import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

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


@dp.message(Command("admin"))
async def admin_panel(message: Message):
    if message.from_user.id != ADMIN_ID:
        return

    users = await db.get_users_count()
    donations = await db.get_donations_count()

    await message.answer(
        f"👨‍💼 Admin panel\n\n"
        f"👥 Foydalanuvchilar: {users}\n"
        f"💰 Donatlar: {donations}"
    )


@dp.message(Command("donate"))
async def donate(message: Message):
    await message.answer(
        "💰 Donat usulini tanlang:",
        reply_markup=keyboards.donate_menu()
    )


@dp.callback_query(lambda c: c.data == "card")
async def card_payment(callback: CallbackQuery):
    await callback.message.answer(
        "💳 Karta orqali to'lov\n\n"
        "Karta raqami:\n"
        "8600 XXXX XXXX XXXX\n\n"
        "Qabul qiluvchi:\n"
        "M.Q\n\n"
        "📸 Chek yuborish shart!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "usdt")
async def usdt_payment(callback: CallbackQuery):
    await callback.message.answer(
        "🪙 USDT TRC20\n\n"
        "Summani tanlang:",
        reply_markup=keyboards.usdt_amount_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "confirm")
async def confirm_payment(callback: CallbackQuery):

    user = callback.from_user

    # Hozircha namuna summa
    await db.add_donation(
        user.id,
        0,
        "unknown"
    )

    if ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"🔔 Yangi donat\n\n"
            f"👤 User: @{user.username}\n"
            f"🆔 ID: {user.id}\n"
            f"⏳ Holat: Tekshirish kerak"
        )

    await callback.message.answer(
        "✅ Donat so'rovi saqlandi.\n"
        "Admin tekshiradi."
    )

    await callback.answer()


async def main():
    await db.init_db()

    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
