import random
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard, get_diary_keyboard

diary_journals = {}

async def handle_diary_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == '📖 Дневник благодарности':
        await show_diary_main_menu(update, context)
    elif text == '📝 Новая запись':
        await start_new_diary_entry(update, context)
    elif text == '📚 Мои записи':
        await show_my_entries(update, context)
    elif text == '🔙 Назад в меню':
        await back_to_main_menu(update, context)
    else:
        await process_diary_text(update, context)

async def show_diary_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    total_entries = get_total_entries_count(user_id)
    today_entries = get_today_entries_count(user_id)
    
    text = f"""
    📖 *Дневник благодарности*

    Привет, {user_name}! 
    За что ты благодарен(на) своему партнеру сегодня?

    📊 *Твоя статистика:*
    • Всего записей: {total_entries}
    • Записей сегодня: {today_entries}

    Выбери действие:
    """
    await update.message.reply_text(text, reply_markup=get_diary_keyboard(), parse_mode='Markdown')

async def start_new_diary_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    📝 *Новая запись благодарности*

    Напиши, за что ты благодарен(на) своему партнеру сегодня.
    Можно написать несколько пунктов.

    *Пример:*
    "Благодарю за утренний кофе в постель"
    "Спасибо за поддержку в трудный момент"
    "Ценю твое чувство юмора сегодня"

    Просто напиши свой текст:
    """
    await update.message.reply_text(text, parse_mode='Markdown')
    
    context.user_data['waiting_for_diary'] = True

async def process_diary_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if context.user_data.get('waiting_for_diary'):
        save_diary_entry(user_id, text)
        
        context.user_data['waiting_for_diary'] = False

        today = datetime.now().strftime("%d.%m.%Y")
        response = f"""
        ✅ *Запись сохранена!*

        📅 *Дата:* {today}
        📝 *Твоя благодарность:*
        {text}

        Твоя благодарность делает отношения крепче! 💖
        """
        await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_diary_keyboard())
    else:
        await show_diary_main_menu(update, context)

async def show_my_entries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    entries = get_recent_entries(user_id, limit=5)
    
    if not entries:
        text = """
        📚 *Мои записи*

        У тебя пока нет записей в дневнике.
        Начни с новой записи! 📝
        """
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_diary_keyboard())
        return
    
    text = "📚 *Твои последние записи:*\n\n"
    
    for i, (date, entry_text) in enumerate(entries, 1):
        text += f"*{i}. {date}:*\n{entry_text}\n\n"
    
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_diary_keyboard())

async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Возвращает в главное меню"""
    await update.message.reply_text(
        "Возвращаемся в главное меню...",
        reply_markup=get_main_keyboard()
    )


def save_diary_entry(user_id: int, text: str):
    """Сохраняет запись благодарности"""
    today = datetime.now().strftime("%d.%m.%Y")
    
    if user_id not in diary_journals:
        diary_journals[user_id] = {}
    
    if today not in diary_journals[user_id]:
        diary_journals[user_id][today] = []
    
    diary_journals[user_id][today].append(text)

def get_total_entries_count(user_id: int) -> int:
    if user_id not in diary_journals:
        return 0
    
    total = 0
    for date_entries in diary_journals[user_id].values():
        total += len(date_entries)
    
    return total

def get_today_entries_count(user_id: int) -> int:
    today = datetime.now().strftime("%d.%m.%Y")
    
    if user_id not in diary_journals or today not in diary_journals[user_id]:
        return 0
    
    return len(diary_journals[user_id][today])

def get_recent_entries(user_id: int, limit: int = 5):
    if user_id not in diary_journals:
        return []
    
    all_entries = []
    for date, entries in diary_journals[user_id].items():
        for entry in entries:
            all_entries.append((date, entry))
    
    all_entries.sort(key=lambda x: datetime.strptime(x[0], "%d.%m.%Y"), reverse=True)
    
    return all_entries[:limit]
