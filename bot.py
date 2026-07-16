import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database as db
import keyboards

from games import GAMES, USD_RATE


logging.basicConfig(level=logging.INFO)


TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


bot = Bot(token=TOKEN)
dp = Dispatcher()


user_orders = {}


@dp.message(Command("start"))
async def start(message: Message):

    await db.init_db()

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
        "🎮 Donat uchun o‘yinni tanlang:",
        reply_markup=keyboards.games_menu()
    )


@dp.callback_query(lambda c: c.data == "choose_game")
async def choose_game(callback: CallbackQuery):

    await callback.message.answer(
        "🎮 O‘yinni tanlang:",
        reply_markup=keyboards.games_menu()
    )

    await callback.answer()

    game_id = callback.data.replace(
        "game_",
        ""
    )

    user_orders[callback.from_user.id] = {
        "game": game_id
    }


    await callback.message.answer(
        "💎 Paketni tanlang:",
        reply_markup=keyboards.packages_menu(game_id)
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data.startswith("package_"))
async def select_package(callback: CallbackQuery):

    data = callback.data.split("_")

    game_id = data[1]
    package_id = int(data[2])


    package = GAMES[game_id]["packages"][package_id]


    user_orders[callback.from_user.id]["package"] = package["name"]
    user_orders[callback.from_user.id]["amount"] = package["usd"]


    await callback.message.answer(
        f"💎 {package['name']}\n\n"
        f"💵 ${package['usd']}\n"
        f"🇺🇿 {package['usd'] * USD_RATE} so'm\n\n"
        "💱 Valyutani tanlang:",
        reply_markup=keyboards.currency_menu()
    )

    await callback.answer()


# 1-QISM TUGADI
@dp.callback_query(lambda c: c.data == "currency_uzs")
async def currency_uzs(callback: CallbackQuery):

    user_orders[callback.from_user.id]["currency"] = "UZS"

    await callback.message.answer(
        "🆔 Player ID yuboring:"
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "currency_usdt")
async def currency_usdt(callback: CallbackQuery):

    user_orders[callback.from_user.id]["currency"] = "USDT"

    await callback.message.answer(
        "🆔 Player ID yuboring:"
    )

    await callback.answer()


@dp.message()
async def get_player_id(message: Message):

    user_id = message.from_user.id

    if user_id not in user_orders:
        return

    if "player_id" not in user_orders[user_id]:

        user_orders[user_id]["player_id"] = message.text

        await message.answer(
            "💳 To‘lov turini tanlang:",
            reply_markup=keyboards.payment_menu()
        )


@dp.callback_query(lambda c: c.data == "payment_card")
async def payment_card(callback: CallbackQuery):

    user_orders[callback.from_user.id]["method"] = "Karta"

    await callback.message.answer(
        "💳 Karta orqali to‘lov\n\n"
        "Karta raqami:\n"
        "8600 XXXX XXXX XXXX\n\n"
        "Qabul qiluvchi: M.Q\n\n"
        "📸 Chek yuboring!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "payment_usdt")
async def payment_usdt(callback: CallbackQuery):

    user_orders[callback.from_user.id]["method"] = "USDT"

    await callback.message.answer(
        "🪙 USDT TRC20\n\n"
        "Hamyon:\n"
        "TXXXXXXXXXXXX\n\n"
        "📸 Chek yuboring!",
        reply_markup=keyboards.confirm_menu()
    )

    await callback.answer()


@dp.callback_query(lambda c: c.data == "confirm")
async def confirm(callback: CallbackQuery):

    order = user_orders.get(callback.from_user.id)

    if not order:
        await callback.message.answer(
            "❌ Buyurtma topilmadi."
        )
        return


    await db.add_order(
        callback.from_user.id,
        order["game"],
        order["package"],
        order["player_id"],
        order["amount"],
        order.get("currency", ""),
        order.get("method", "")
    )


    if ADMIN_ID:

        await bot.send_message(
            ADMIN_ID,
            f"🔔 Yangi buyurtma\n\n"
            f"🎮 O‘yin: {order['game']}\n"
            f"💎 Paket: {order['package']}\n"
            f"🆔 ID: {order['player_id']}\n"
            f"💰 ${order['amount']}\n"
            f"💳 {order.get('method','')}"
        )


    await callback.message.answer(
        "✅ Donat so‘rovi saqlandi.\n"
        "Admin tekshiradi."
    )

    await callback.answer()



async def main():

    await db.init_db()

    print("Bot ishga tushdi")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
