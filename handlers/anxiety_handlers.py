from telegram import Update
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard, get_anxiety_keyboard, get_anxiety_techniques_keyboard
from data.anxiety_data import anxiety_techniques, anxiety_categories

async def handle_anxiety_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    anxiety_main_buttons = [
        '🌬️ Дыхательные техники', 
        '🌍 5-4-3-2-1', 
        '💪 Физические техники',
        '🔙 Назад'
    ]
    
    all_technique_names = []
    for category in anxiety_techniques.values():
        for technique in category['techniques']:
            all_technique_names.append(technique['name'])
    
    if text == '😰 Тревожность':
        await show_anxiety_main_menu(update, context)
        return True
    
    if text in anxiety_main_buttons:
        await handle_anxiety_selection(update, context, text)
        return True
    
    if text in all_technique_names:
        await show_technique_details(update, context)
        return True
    
    return False


async def show_anxiety_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает главное меню помощи при тревожности."""
    text = """
😰 *Помощь при тревожности*

Здесь вы найдете проверенные техники для снижения тревоги и управления стрессом.

*Выберите нужный раздел:*
    """
    
    await update.message.reply_text(text, reply_markup=get_anxiety_keyboard(), parse_mode='Markdown')

async def handle_anxiety_selection(update: Update, context: ContextTypes.DEFAULT_TYPE, button_text: str):
    """Обрабатывает выбор раздела помощи при тревожности."""
    if button_text == '🌬️ Дыхательные техники':
        await show_anxiety_techniques(update, context, 'breathing')
    elif button_text == '🌍 5-4-3-2-1':
        await show_anxiety_techniques(update, context, 'grounding')
    elif button_text == '💪 Физические техники':
        await show_anxiety_techniques(update, context, 'physical')


async def show_anxiety_techniques(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str):
    category_data = anxiety_techniques[category]
    
    text = f"""
{category_data['title']}

*{category_data['description']}*

*Выберите технику:*
    """
    
    context.user_data['current_anxiety_category'] = category
    
    await update.message.reply_text(
        text, 
        parse_mode='Markdown',
        reply_markup=get_anxiety_techniques_keyboard(category)
    )

async def show_technique_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    current_category = context.user_data.get('current_anxiety_category')
    if not current_category:
        await show_anxiety_main_menu(update, context)
        return
    
    category_data = anxiety_techniques[current_category]
    
    selected_technique = None
    for technique in category_data['techniques']:
        if technique['name'] == text:
            selected_technique = technique
            break
    
    if not selected_technique:
        await show_anxiety_techniques(update, context, current_category)
        return
    
    steps_text = ""
    for i, step in enumerate(selected_technique['steps'], 1):
        steps_text += f"{i}. {step}\n"
    
    technique_text = f"""
🧘 *{selected_technique['name']}*

*Шаги выполнения:*
{steps_text}

💡 *Совет:* {selected_technique['tip']}

*Начните выполнять технику прямо сейчас!*
    """
    
    await update.message.reply_text(technique_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')