from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_truth_or_dare_keyboard
import random
from data.truth_or_dare import truth_questions, dare_actions

async def truth_or_dare_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
    🎲 *Правда или Действие*
    
    Добро пожаловать в игру - Правда или Действие!
    
    Выберите действие:
    """
    await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')

async def truth_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(truth_questions)
    text = f"🎲 *Правда или Действие?*\n\n*Правда:*\n{item}"

    await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')

async def dare_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = random.choice(dare_actions)
    text = f"🎲 *Правда или Действие?*\n\n*Действие:*\n{item}"

    await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')
