from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Create main menu keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="# Катигории", callback_data="menu"),
            InlineKeyboardButton(text="🛒 Моя корзина", callback_data="cart")
        ],
        [
            InlineKeyboardButton(text="📞 Контакты", callback_data="contact"),
            InlineKeyboardButton(text="📍 Локация", callback_data="location")
        ],
        [
            InlineKeyboardButton(text="⏰ Часы", callback_data="hours")
        ]
    ])
    return keyboard

def get_back_keyboard():
    """Create back to main menu keyboard"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в катигории", callback_data="back")]
    ])
    return keyboard