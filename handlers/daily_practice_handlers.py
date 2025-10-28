from telegram.ext import ContextTypes
from telegram import Update
import random
from data.motivational_quotes import motivational_quotes
from data.affirmations import relationship_affirmations
from utils.keyboards import get_main_keyboard, get_settings_keyboard
import logging

logger = logging.getLogger(__name__)

subscribed_users = set()

async def send_daily_practice(context: ContextTypes.DEFAULT_TYPE):
    if not subscribed_users:
        logger.info("Нет пользователей с активной ежедневной рассылкой")
        return
    
    logger.info(f"Отправка ежедневной практики для {len(subscribed_users)} пользователей")
    
    for user_id in list(subscribed_users): 
        try:
            user = await context.bot.get_chat(user_id)
            first_name = user.first_name
            
            choice = random.choice(['motivation', 'affirmation'])
            
            if choice == 'motivation':
                quote = random.choice(motivational_quotes)
                message = f"🌅 Доброе утро, {first_name}!\n\n💫 *Мотивация на сегодня:*\n\n{quote}"
            else:
                affirmation = random.choice(relationship_affirmations)
                message = f"🌅 Доброе утро, {first_name}!\n\n💝 *Аффирмация для вас:*\n\n{affirmation}"
            
            await context.bot.send_message(chat_id=user_id, text=message, parse_mode='Markdown')
            logger.info(f"Сообщение отправлено пользователю {user_id}")
            
        except Exception as e:
            logger.error(f"Ошибка отправки пользователю {user_id}: {e}")
            if "bot was blocked" in str(e).lower():
                subscribed_users.discard(user_id)
                logger.info(f"Пользователь {user_id} удален из рассылки (заблокировал бота)")

async def daily_practice_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    status = "включена" if user_id in subscribed_users else "выключена"
    
    text = f"""
    ⚙️ *Настройки ежедневной рассылки*
    
    Текущий статус: {status}
    
    Выберите действие:
    """
    await update.message.reply_text(text, reply_markup=get_settings_keyboard(), parse_mode='Markdown')

async def enable_daily_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribed_users.add(user_id)
    
    await update.message.reply_text(
        "✅ *Ежедневная рассылка включена!*\n\n"
        "Теперь вы будете получать ежедневные уведомления.",
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown',
    )

async def disable_daily_practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    subscribed_users.discard(user_id)
    
    await update.message.reply_text(
        "❌ *Ежедневная рассылка отключена!*\n\n"
        "Вы больше не будете получать ежедневные уведомления.",
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )