from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from games import GAMES


def donate_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 O‘yin donati",
                    callback_data="choose_game"
                )
            ]
        ]
    )


def games_menu():
    buttons = []

    for game_id, game in GAMES.items():
        buttons.append([
            InlineKeyboardButton(
                text=game["name"],
                callback_data=f"game_{game_id}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def packages_menu(game_id):
    buttons = []

    for index, package in enumerate(GAMES[game_id]["packages"]):
        buttons.append([
            InlineKeyboardButton(
                text=f"💎 {package['name']}",
                callback_data=f"package_{game_id}_{index}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def currency_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇿 UZS (So'm)",
                    callback_data="currency_uzs"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🪙 USDT",
                    callback_data="currency_usdt"
                )
            ]
        ]
    )


def payment_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Karta orqali",
                    callback_data="payment_card"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🪙 USDT orqali",
                    callback_data="payment_usdt"
                )
            ]
        ]
    )


def confirm_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📸 Chek yubordim ✅",
                    callback_data="confirm"
                )
            ]
        ]
    )
