from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    🚪 *Выход*
    
    Спасибо, что воспользовались нашим ботом!
    Если захотите вернуться, просто отправьте команду /start
    
    Хорошего дня! 🌟
    """

    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=ReplyKeyboardRemove())