from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def donate_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Karta orqali",
                    callback_data="card"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🪙 USDT orqali",
                    callback_data="usdt"
                )
            ]
        ]
    )


def confirm_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Tasdiqladim",
                    callback_data="confirm"
                )
            ]
        ]
    )


def usdt_amount_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="10 USDT", callback_data="usdt_10")
            ],
            [
                InlineKeyboardButton(text="25 USDT", callback_data="usdt_25")
            ],
            [
                InlineKeyboardButton(text="50 USDT", callback_data="usdt_50")
            ],
            [
                InlineKeyboardButton(text="100 USDT", callback_data="usdt_100")
            ]
        ]
    )
