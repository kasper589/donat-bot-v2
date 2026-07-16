import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

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
        "🔥 Free Fire Donat bot\n\n"
        "/donate - donat qilish"
    )


@dp.message(Command("donate"))
async def donate(message: Message):

    await message.answer(
        "🎮 O‘yinni tanlang:",
        reply_markup=keyboards.games_menu()
    )


@dp.callback_query(lambda c: c.data.startswith("game_"))
async def select_game(callback: CallbackQuery):

    game_id = callback.data.replace(
        "game_",
        ""
    )

    user_orders[callback.from_user.id] = {
        "game": game_id
    }


    await callback.message.answer(
        "💎 Diamond paketni tanlang:",
        reply_markup=keyboards.packages_menu(game_id)
    )

    await callback.answer()



@dp.callback_query(lambda c: c.data.startswith("package_"))
async def select_package(callback: CallbackQuery):

    data = callback.data.split("_")

    package_id = int(data[-1])
    game_id = "_".join(data[1:-1])


    package = GAMES[game_id]["packages"][package_id]


    user_orders[callback.from_user.id]["package"] = package["name"]
    user_orders[callback.from_user.id]["amount"] = package["usd"]


    await callback.message.answer(
        f"💎 {package['name']}\n\n"
        f"💵 ${package['usd']}\n"
        f"🇺🇿 {package['usd'] * USD_RATE} so‘m\n\n"
        "💱 Valyutani tanlang:",
        reply_markup=keyboards.currency_menu()
    )


    await callback.answer()



@dp.callback_query(lambda c: c.data == "currency_uzs")
async def currency_uzs(callback: CallbackQuery):

    user_orders[callback.from_user.id]["currency"] = "UZS"

    await callback.message.answer(
        "🆔 Free Fire ID yuboring:"
    )

    await callback.answer()



@dp.callback_query(lambda c: c.data == "currency_usdt")
async def currency_usdt(callback: CallbackQuery):

    user_orders[callback.from_user.id]["currency"] = "USDT"

    await callback.message.answer(
        "🆔 Free Fire ID yuboring:"
    )
    await callback.answer()
    @dp.message()
async def get_player_id(message: Message):
    uid = message.from_user.id

    if uid not in user_orders:
        return


    if "player_id" not in user_orders[uid]:

        user_orders[uid]["player_id"] = message.text


        await message.answer(
            "💳 To‘lov turini tanlang:",
            reply_markup=keyboards.payment_menu()
        )



@dp.callback_query(lambda c: c.data == "payment_card")
async def payment_card(callback: CallbackQuery):

    user_orders[callback.from_user.id]["method"] = "Karta"


    await callback.message.answer(
        "💳 Karta orqali to‘lov\n\n"
        "8600 XXXX XXXX XXXX\n\n"
        "📸 Chek rasmini yuboring."
    )


    await callback.answer()



@dp.callback_query(lambda c: c.data == "payment_usdt")
async def payment_usdt(callback: CallbackQuery):

    user_orders[callback.from_user.id]["method"] = "USDT"


    await callback.message.answer(
        "🪙 USDT TRC20\n\n"
        "Wallet:\n"
        "TXXXXXXXXXXXX\n\n"
        "📸 Chek rasmini yuboring."
    )


    await callback.answer()



@dp.message()
async def get_check(message: Message):

    uid = message.from_user.id


    if uid not in user_orders:
        return


    order = user_orders[uid]


    if message.photo:


        await db.add_order(
            uid,
            order["game"],
            order["package"],
            order["player_id"],
            order["amount"],
            order.get("currency", ""),
            order.get("method", "")
        )


        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Tasdiqlash",
                        callback_data=f"approve_{uid}"
                    ),
                    InlineKeyboardButton(
                        text="❌ Rad etish",
                        callback_data=f"reject_{uid}"
                    )
                ]
            ]
        )


        if ADMIN_ID:

            await bot.send_photo(
                ADMIN_ID,
                message.photo[-1].file_id,
                caption=(
                    "🔥 Yangi buyurtma\n\n"
                    f"👤 User: {uid}\n"
                    f"🎮 O‘yin: {order['game']}\n"
                    f"💎 Paket: {order['package']}\n"
                    f"🆔 ID: {order['player_id']}\n"
                    f"💰 ${order['amount']}"
                ),
                reply_markup=keyboard
            )


        await message.answer(
            "✅ Chek qabul qilindi.\n"
            "Admin tekshiradi."
        )


    else:

        await message.answer(
            "📸 Iltimos, chek rasmini yuboring."
        )



@dp.callback_query(lambda c: c.data.startswith("approve_"))
async def approve(callback: CallbackQuery):

    uid = int(
        callback.data.replace(
            "approve_",
            ""
        )
    )


    await bot.send_message(
        uid,
        "✅ To‘lov tasdiqlandi!"
    )


    await callback.message.edit_caption(
        caption="✅ Buyurtma tasdiqlandi."
    )


    await callback.answer()



@dp.callback_query(lambda c: c.data.startswith("reject_"))
async def reject(callback: CallbackQuery):

    uid = int(
        callback.data.replace(
            "reject_",
            ""
        )
    )


    await bot.send_message(
        uid,
        "❌ To‘lov rad etildi."
    )


    await callback.message.edit_caption(
        caption="❌ Buyurtma rad etildi."
    )


    await callback.answer()



async def main():

    await db.init_db()

    print("Bot ishga tushdi")

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
