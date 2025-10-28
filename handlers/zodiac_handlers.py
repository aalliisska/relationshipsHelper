from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard, get_zodiac_keyboard
from data.zodiac_compatibility import zodiac_compatibility, zodiac_signs

async def show_zodiac_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    ♌️ *Тест на совместимость по знакам Зодиака*

    Узнайте, насколько гармонично сочетаются ваши знаки зодиака!

    *Как это работает:*
    • Введите два знака зодиака через пробел

    *Пример:* `Овен Весы` или `Телец Скорпион`

    Выберите действие:
    """

    context.user_data['waiting_for_zodiac_input'] = True
    context.user_data['zodiac_step'] = 1 

    await update.message.reply_text(text, reply_markup=get_zodiac_keyboard(), parse_mode='Markdown')

async def process_zodiac_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if context.user_data.get('zodiac_step') == 2:
        first_sign = context.user_data.get('first_sign')
        signs_found = []
        
        for sign in zodiac_signs:
            if sign.lower() in text.lower():
                signs_found.append(sign)
        
        if signs_found:
            second_sign = signs_found[0]
            await check_compatibility(update, first_sign, second_sign)
            context.user_data.pop('waiting_for_zodiac_input', None)
            context.user_data.pop('zodiac_step', None)
            context.user_data.pop('first_sign', None)
        else:
            await update.message.reply_text(
                "❌ Не удалось распознать знак зодиака. Пожалуйста, введите второй знак:",
                parse_mode='Markdown'
            )
        return
    
    signs_found = []
    for sign in zodiac_signs:
        if sign.lower() in text.lower():
            signs_found.append(sign)
    
    if len(signs_found) >= 2:
        await check_compatibility(update, signs_found[0], signs_found[1])
        context.user_data.pop('waiting_for_zodiac_input', None)
        context.user_data.pop('zodiac_step', None)
        
    elif len(signs_found) == 1:
        context.user_data['first_sign'] = signs_found[0]
        context.user_data['zodiac_step'] = 2
        
        text = f"""
✅ *Первый знак:* {signs_found[0]}

Теперь введите второй знак зодиака:
        """
        await update.message.reply_text(text, parse_mode='Markdown')
        
    else:
        await update.message.reply_text(
            "❌ Не удалось распознать знаки зодиака. Пожалуйста, введите два знака через пробел:\n\n*Пример:* Овен Телец",
            parse_mode='Markdown'
        )

async def check_compatibility(update: Update, sign1: str, sign2: str):
    pair1 = f"{sign1} - {sign2}"
    pair2 = f"{sign2} - {sign1}"
    
    compatibility = None
    for comp in zodiac_compatibility:
        if comp["pair"] == pair1 or comp["pair"] == pair2:
            compatibility = comp
            break
    
    if compatibility:
        percentage = compatibility["percentage"]
        pair = compatibility["pair"]
        
        if percentage >= 90:
            emoji = "💖"
            rating = "ИДЕАЛЬНАЯ СОВМЕСТИМОСТЬ"
        elif percentage >= 70:
            emoji = "💕"
            rating = "ОТЛИЧНАЯ СОВМЕСТИМОСТЬ"
        elif percentage >= 50:
            emoji = "💝"
            rating = "ХОРОШАЯ СОВМЕСТИМОСТЬ"
        else:
            emoji = "💔"
            rating = "СЛОЖНАЯ СОВМЕСТИМОСТЬ"
        
        response = f"""
{emoji} *СОВМЕСТИМОСТЬ: {percentage}%*
*Пара:* {pair}
*Рейтинг:* {rating}

🌟 *Сильные стороны:*
{compatibility["strengths"]}

⚡ *Сложности:*
{compatibility["challenges"]}

💑 *Любовь и отношения:*
{compatibility["love"]}

👫 *Дружба:*
{compatibility["friendship"]}

💼 *Карьера и бизнес:*
{compatibility["career"]}

💡 *Совет для пары:*
{compatibility["advice"]}

*Помните:* Совместимость по знакам зодиака - это лишь ориентир!
Настоящие отношения строятся на взаимном уважении и любви. 💫
        """
    else:
        response = f"""
❌ *Совместимость не найдена*

Для пары *{sign1} - {sign2}* пока нет данных о совместимости.
Попробуйте другую комбинацию знаков.
        """
    
    await update.message.reply_text(response, parse_mode='Markdown', reply_markup=get_main_keyboard())

async def show_all_zodiac_signs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    
    text = f"""
*Даты знаков:*
• Овен: 21 марта - 19 апреля
• Телец: 20 апреля - 20 мая  
• Близнецы: 21 мая - 20 июня
• Рак: 21 июня - 22 июля
• Лев: 23 июля - 22 августа
• Дева: 23 августа - 22 сентября
• Весы: 23 сентября - 22 октября
• Скорпион: 23 октября - 21 ноября
• Стрелец: 22 ноября - 21 декабря
• Козерог: 22 декабря - 19 января
• Водолей: 20 января - 18 февраля
• Рыбы: 19 февраля - 20 марта
    """
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())
