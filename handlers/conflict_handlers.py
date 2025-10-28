from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from utils.keyboards import get_main_keyboard, get_conflict_keyboard
from data.conflict_data import nvc_steps

async def show_conflict_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    🚨 *У нас ссора*

    Я помогу вам конструктивно решить конфликт с помощью метода *Ненасильственного Общения* (ННО).

    📋 *4 шага ННО:*
    1. 📝 *Наблюдения* - факты без оценок
    2. 💖 *Чувства* - ваши эмоции
    3. 🎯 *Потребности* - что важно для вас
    4. 🙏 *Просьба* - конкретное действие

    *Результат:* Готовая фраза для разговора с партнером

    Выберите действие:
    """
    await update.message.reply_text(text, reply_markup=get_conflict_keyboard(), parse_mode='Markdown')

async def start_nvc_process(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['nvc_data'] = {
        'current_step': 1,
        'answers': {}
    }
    
    await show_nvc_step(update, context)

async def show_nvc_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nvc_data = context.user_data.get('nvc_data', {})
    current_step = nvc_data.get('current_step', 1)
    
    if current_step > len(nvc_steps):
        await show_final_phrase(update, context)
        return
    
    step_info = nvc_steps[current_step - 1]
    
    text = f"""
    *Шаг {step_info['step']}: {step_info['title']}*

    {step_info['question']}

    {step_info['example']}

    ✍️ *Напишите ваш ответ:*
    """
    
    keyboard = [['🔙 Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def process_nvc_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nvc_data = context.user_data.get('nvc_data', {})
    current_step = nvc_data.get('current_step', 1)
    
    if current_step > len(nvc_steps):
        return
    
    user_answer = update.message.text
    step_info = nvc_steps[current_step - 1]
    
    nvc_data['answers'][step_info['key']] = user_answer
    context.user_data['nvc_data'] = nvc_data
    
    nvc_data['current_step'] += 1
    context.user_data['nvc_data'] = nvc_data
    
    await show_nvc_step(update, context)

async def show_final_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nvc_data = context.user_data.get('nvc_data', {})
    answers = nvc_data.get('answers', {})

    observation = answers.get('observation', '')
    feelings = answers.get('feelings', '')
    needs = answers.get('needs', '')
    request = answers.get('request', '')
    
    final_phrase = f"""
    💫 *Готовая фраза для разговора:*

    «Когда {observation}, 
    я чувствую {feelings}, 
    потому что мне важно {needs}. 
    Не мог(ла) бы ты {request}?»

    🌟 *Советы для разговора:*
    • Говорите спокойным тоном
    • Выберите подходящее время
    • Слушайте ответ партнера
    • Будьте открыты к компромиссу

    *Помните:* Цель - не победить в споре, а понять друг друга и найти решение!
    """
    
    await update.message.reply_text(final_phrase, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    context.user_data.pop('nvc_data', None)

async def show_example_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    examples = [
        {
            "situation": "💔 Партнер забыл о важной дате",
            "phrase": "«Когда ты забыл о нашей годовщине, я почувствовал(а) грусть и разочарование, потому что для меня важны наши традиции и внимание друг к другу. Мог(ла) бы ты в следующий раз отметить эту дату в календаре?»"
        },
        {
            "situation": "😠 Партнер перебивает во время разговора",
            "phrase": "«Когда ты перебиваешь меня во время разговора, я чувствую раздражение и неуважение, потому что мне важно, чтобы мое мнение тоже было услышано. Не мог(ла) бы ты давать мне закончить мысль?»"
        },
        {
            "situation": "📱 Партнер постоянно в телефоне",
            "phrase": "«Когда ты проводишь много времени в телефоне, пока мы вместе, я чувствую одиночество и ненужность, потому что мне важно наше качественное время. Мог(ла) бы ты откладывать телефон, когда мы общаемся?»"
        }
    ]
    
    text = "📋 *Примеры готовых фраз по методу ННО:*\n\n"
    
    for example in examples:
        text += f"*{example['situation']}*\n"
        text += f"{example['phrase']}\n\n"
    
    text += "💡 *Используйте эти примеры как шаблон для своих ситуаций!*"
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())

async def explain_nvc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Объясняет что такое Ненасильственное Общение"""
    text = """
    💡 *Что такое Ненасильственное Общение (ННО)?*

    ННО — это метод общения, разработанный психологом Маршаллом Розенбергом, который помогает:

    • 🗣️ *Выражать себя* честно и ясно
    • 👂 *Слушать других* с уважением и пониманием  
    • 🤝 *Разрешать конфликты* мирным путем
    • 💖 *Строить отношения* на основе взаимного уважения

    📚 *4 компонента ННО:*

    1. *Наблюдения* 📝
    - Факты без оценок и интерпретаций
    - «Что я вижу/слышу?»

    2. *Чувства* 💖  
    - Наши эмоции в ответ на ситуацию
    - «Что я чувствую?»

    3. *Потребности* 🎯
    - Наши глубинные ценности и желания
    - «Что для меня важно?»

    4. *Просьбы* 🙏
    - Конкретные, выполнимые действия
    - «О чем я прошу?»

    🌟 *Преимущества ННО:*
    • Уменьшает защитную реакцию
    • Создает атмосферу доверия
    • Помогает найти взаимовыгодные решения
    • Укрепляет эмоциональную связь

    *Попробуйте ННО в ваших отношениях!* ✨
    """
    
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=get_main_keyboard())
