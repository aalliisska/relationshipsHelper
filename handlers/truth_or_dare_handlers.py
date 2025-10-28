from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_truth_or_dare_keyboard, get_categories_keyboard
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
    context.user_data['current_game'] = 'truth'

    text = f"🎲 *Правда или Действие?*\n\n*Правда:*\n\nВыберите категорию вопросов:"

    categories = [category["category"] for category in truth_questions]
    categories.append("🔄 Перемешать всё")

    await update.message.reply_text(text, reply_markup=get_categories_keyboard(categories), parse_mode='Markdown')

async def dare_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['current_game'] = 'dare'

    text = f"🎲 *Правда или Действие?*\n\n*Действие:*\n\nВыберите категорию действий:"

    categories = [category["category"] for category in dare_actions]
    categories.append("🔄 Перемешать всё")

    await update.message.reply_text(text, reply_markup=get_categories_keyboard(categories), parse_mode='Markdown')


async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected_category = update.message.text
    game_type = context.user_data.get('current_game', 'truth')
    
    if selected_category == "🔄 Перемешать всё":
        if game_type == 'truth':
            all_questions = []
            for category in truth_questions:
                all_questions.extend(category["questions"])
            item = random.choice(all_questions)
            text = f"🎲 *Правда или Действие?*\n\n*Правда (случайная категория):*\n\n{item}"
        else:
            all_actions = []
            for category in dare_actions:
                all_actions.extend(category["actions"])
            item = random.choice(all_actions)
            text = f"🎲 *Правда или Действие?*\n\n*Действие (случайная категория):*\n\n{item}"
            
        await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')
        return
    
    if game_type == 'truth':
        category_data = next((cat for cat in truth_questions if cat["category"] == selected_category), None)
        if category_data:
            item = random.choice(category_data["questions"])
            text = f"🎲 *Правда или Действие?*\n\n*Правда ({selected_category}):*\n\n{item}"
            await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Категория не найдена", reply_markup=get_truth_or_dare_keyboard())
    else:
        category_data = next((cat for cat in dare_actions if cat["category"] == selected_category), None)
        if category_data:
            item = random.choice(category_data["actions"])
            text = f"🎲 *Правда или Действие?*\n\n*Действие ({selected_category}):*\n\n{item}"
            await update.message.reply_text(text, reply_markup=get_truth_or_dare_keyboard(), parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ Категория не найдена", reply_markup=get_truth_or_dare_keyboard())