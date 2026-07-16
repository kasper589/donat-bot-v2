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

user_payments = {}

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
        "/donate - donat qilish"
    )


@dp.message(Command("donate"))
async def donate(message: Message):
    await message.answer(
        "💰 To'lov usulini tanlang:",
        reply_markup=keyboards.donate_menu()
    )


@dp.callback_query(lambda c: c.data == "card")
async def card(callback: CallbackQuery):
    await callback.message.answer(
        "💳 Karta orqali to'lov\n\n"
        "Valyutani tanlang:",
        reply_markup=keyboards.currency_menu()
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "uzs")
async def uzs(callback: CallbackQuery):
    await callback.message.answer(
        "🇺🇿 Summani tanlang:",
        reply_markup=keyboards.uzs_amount_menu()
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data == "usdt_currency")
async def usdt(callback: CallbackQuery):
    await callback.message.answer(
        "🪙 USDT summani tanlang:",
        reply_markup=keyboards.usdt_amount_menu()
    )
    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("uzs_"))
async def uzs_amount(callback: CallbackQuery):
    amount = callback.data.replace("uzs_", "")

    user_payments[callback.from_user.id] = {
        "amount": amount,
        "currency": "UZS",
        "method": "Karta"
    }

    await callback.message.answer(
        f"💳 Karta raqami:\n"
        f"8600 XXXX XXXX XXXX\n\n"
        f"💰 Summa: {amount} UZS\n\n"
        "📸 Chek yuborish shart!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("usdt_"))
async def usdt_amount(callback: CallbackQuery):
    amount = callback.data.replace("usdt_", "")

    user_payments[callback.from_user.id] = {
        "amount": amount,
        "currency": "USDT",
        "method": "USDT TRC20"
    }

    await callback.message.answer(
        f"🪙 USDT: {amount}\n\n"
        "Hamyon:\n"
        "TXXXXXXXXXXXX\n\n"
        "📸 Chek yuborish shart!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "confirm")
async def confirm(callback: CallbackQuery):
    user_id = callback.from_user.id

    payment = user_payments.get(user_id)

    if not payment:
        await callback.message.answer(
            "❌ Avval summa tanlang."
        )
        return

    await db.add_donation(
        user_id,
        payment["amount"],
        payment["currency"],
        payment["method"]
    )

    if ADMIN_ID:
        await bot.send_message(
            ADMIN_ID,
            f"🔔 Yangi donat\n\n"
            f"👤 ID: {user_id}\n"
            f"💰 {payment['amount']} {payment['currency']}\n"
            f"💳 {payment['method']}"
        )

    await callback.message.answer(
        "✅ Donat saqlandi.\nAdmin tekshiradi."
    )

    await callback.answer()


async def main():
    await db.init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
