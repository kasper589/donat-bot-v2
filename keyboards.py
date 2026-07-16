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


def currency_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇿 UZS",
                    callback_data="uzs"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🪙 USDT",
                    callback_data="usdt_currency"
                )
            ]
        ]
    )


def uzs_amount_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="50 000 UZS",
                    callback_data="uzs_50000"
                )
            ],
            [
                InlineKeyboardButton(
                    text="100 000 UZS",
                    callback_data="uzs_100000"
                )
            ],
            [
                InlineKeyboardButton(
                    text="500 000 UZS",
                    callback_data="uzs_500000"
                )
            ]
        ]
    )


def usdt_amount_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="10 USDT",
                    callback_data="usdt_10"
                )
            ],
            [
                InlineKeyboardButton(
                    text="25 USDT",
                    callback_data="usdt_25"
                )
            ],
            [
                InlineKeyboardButton(
                    text="50 USDT",
                    callback_data="usdt_50"
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
