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
        "📸 Chek yuborish shart!\n\n"
        "To'lov qilgach pastdagi tugmani bosing.",
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


@dp.callback_query(lambda c: c.data.startswith("usdt_"))
async def usdt_amount(callback: CallbackQuery):
    amount = callback.data.replace("usdt_", "")

    await callback.message.answer(
        f"🪙 {amount} USDT\n\n"
        "TRC20 manzil:\n"
        "TXXXXXXXXXXXX\n\n"
        "Tarmoq: TRC20\n\n"
        "📸 Chek yuborish shart!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "confirm")
async def confirm_payment(callback: CallbackQuery):
    user = callback.from_user

    admin_text = (
        "🔔 Yangi donat tekshiruvi\n\n"
        f"👤 Username: @{user.username}\n"
        f"🆔 ID: {user.id}\n\n"
        "⏳ Holat: Tekshirish kerak"
    )

    if ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            admin_text
        )

    await callback.message.answer(
        "✅ Tasdiqlash so'rovi yuborildi.\n\n"
        "Admin tekshirganidan so'ng tasdiqlanadi."
    )

    await callback.answer()


@dp.message()
async def other(message: Message):
    await message.answer(
        "Xabaringiz qabul qilindi ✅"
    )


async def main():
    await db.init_db()

    logging.info("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
