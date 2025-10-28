from telegram import Update,  ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Вот что я умею:

    *♌️ Тест на совместимость* - Узнайте, насколько гармонично сочетаются ваши знаки зодиака.
    *🚨 У нас ссора* - Пройдите по шагам Ненасильственного Общения, чтобы конструктивно решить конфликт.
    *😰 Тревожность* - Используйте техники (дыхание, 5-4-3-2-1), чтобы снизить тревогу.
    *💬 Время для разговора* - Когда хочешь узнать партнера поближе, но не знаешь с чего начать.
    *🎲 Правда или Действие* - Веселая игра для пар, чтобы стать ближе.

    Просто нажми на одну из кнопок в меню!
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')