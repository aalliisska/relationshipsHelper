from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    welcome_text = f"""
    Привет, {user_name}! 👋
    Я — твой бот-помощник в сфере отношений.
    Я здесь, чтобы поддержать тебя, помочь лучше понять партнера и укрепить вашу связь.

    Выбери нужный раздел в меню ниже:
    """
    await update.message.reply_text(welcome_text, reply_markup=get_main_keyboard())