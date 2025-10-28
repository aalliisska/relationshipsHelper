import logging
import random
from datetime import time
import pytz
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import BOT_TOKEN
from data.questions import questions
#from task2.archive.diary import handle_diary_menu
from utils.keyboards import get_main_keyboard
from handlers.zodiac_handlers import show_zodiac_main_menu, process_zodiac_input, show_all_zodiac_signs
from handlers.anxiety_handlers import handle_anxiety_flow
from handlers.conflict_handlers import show_conflict_main_menu, start_nvc_process, show_example_phrase, explain_nvc, process_nvc_step
from data.conflict_data import nvc_steps
from handlers.help_command_handlers import help_command
from handlers.start_handlers import start
from handlers.truth_or_dare_handlers import truth_or_dare_game, truth_game, dare_game, handle_category_selection
from handlers.exit_handlers import exit
from handlers.daily_practice_handlers import send_daily_practice, daily_practice_settings, enable_daily_practice, disable_daily_practice
from data.truth_or_dare import truth_questions, dare_actions


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


DAILY_TIME = time(hour=9, minute=0, tzinfo=pytz.timezone('Europe/Moscow'))

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == '🔙 Назад':
        context.user_data.clear()
        await update.message.reply_text('Пожалуйста, выберите опцию из меню ниже:', parse_mode='Markdown', reply_markup=get_main_keyboard())
        
    elif text == '📋 Все знаки зодиака':
        await show_all_zodiac_signs(update, context)
        return
    
    if context.user_data.get('waiting_for_zodiac_input'):
        await process_zodiac_input(update, context)
        return
    
    if await handle_anxiety_flow(update, context):
        return
    
    nvc_data = context.user_data.get('nvc_data', {})
    current_step = nvc_data.get('current_step', 0)

    if current_step > 0 and current_step <= len(nvc_steps):
        await process_nvc_step(update, context)
        return
    
    all_truth_categories = [cat["category"] for cat in truth_questions]
    all_dare_categories = [cat["category"] for cat in dare_actions]
    all_categories = all_truth_categories + all_dare_categories + ["🔄 Перемешать всё"]
    
    if text in all_categories:
        await handle_category_selection(update, context)
        return
    
    if text == '💬 Время для разговора':
        question = random.choice(questions)
        await update.message.reply_text(f"⭐ Вопрос для сближения:\n\n{question}")
    
#    elif text == '📖 Дневник благодарности':
#        await handle_diary_menu(update, context)
#   elif text.startswith('📅 ') or text in ['📝 Новая запись', '📚 Мои записи']:
#       await handle_diary_menu(update, context)

    elif text == '♌️ Тест на совместимость':
        await show_zodiac_main_menu(update, context)

    elif text == '🚨 У нас ссора':
        await show_conflict_main_menu(update, context)

    elif text == '🔄 Начать':
        await start_nvc_process(update, context)

    elif text == '📋 Пример готовой фразы':
        await show_example_phrase(update, context)

    elif text == '💡 Что такое ННО?':
        await explain_nvc(update, context)

    elif text == '🎲 Правда или Действие':
        await truth_or_dare_game(update, context)

    elif text == '💬 Правда':
        await truth_game(update, context)

    elif text == '🚀 Действие':
        await dare_game(update, context)

    elif text == '⚙️ Настройки рассылки':
        await daily_practice_settings(update, context)

    elif text == '✅ Включить рассылку':
        await enable_daily_practice(update, context)
    
    elif text == '❌ Выключить рассылку':
        await disable_daily_practice(update, context)

    elif text == 'ℹ️ Что я умею':
        await help_command(update, context)
    
    elif text == '🚪 Выход':
        await exit(update, context)
    else:
        await update.message.reply_text("Пожалуйста, выберите опцию из меню ниже:", reply_markup=get_main_keyboard())

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    job_queue = application.job_queue
    job_queue.run_daily(
        send_daily_practice,
        DAILY_TIME,
        name="daily_practice"
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    logger.info("Бот запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()