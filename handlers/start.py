from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_keyboard import get_main_keyboard

# Create router instance
router = Router()

@router.message(CommandStart())
async def start_handler(message: Message):
    """Handle /start command"""
    await message.answer(
        f"👋 Привет, {message.from_user.full_name}!\n"
        f"Добро пожаловать в Style Shop Bot!\n\n"
        f"Я могу тебе помочь:\n"
        f"🏪 Просмотреть наши одежды и обуви\n"
        f"📞 Получить контактную информацию\n"
        f"📍 Найти наше местоположение\n"
        f"⏰ Проверить время работы",
        reply_markup=get_main_keyboard()
    )