from telegram import ReplyKeyboardMarkup
from data.anxiety_data import anxiety_techniques

def get_main_keyboard():
    keyboard = [
        ['♌️ Тест на совместимость'],
        ['🚨 У нас ссора'],
        ['😰 Тревожность'],
        ['💬 Время для разговора'],
        #['📖 Дневник благодарности'],
        #['✅ Чек-лист отношений'],
        ['🎲 Правда или Действие'],
        ['⚙️ Настройки рассылки'],
        ['ℹ️ Что я умею'],
        ['🚪 Выход']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_truth_or_dare_keyboard():
    keyboard = [
        ['💬 Правда'],
        ['🚀 Действие'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_categories_keyboard(categories):
    keyboard = []

    for i in range(0, len(categories), 2):
        row = []
        if i < len(categories):
            row.append(categories[i])
        if i + 1 < len(categories):
            row.append(categories[i + 1])
        keyboard.append(row)

    keyboard.append(['🔙 Назад'])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_settings_keyboard():
    keyboard = [
        ['✅ Включить рассылку'],
        ['❌ Выключить рассылку'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_zodiac_keyboard():
    keyboard = [
        ['📋 Все знаки зодиака'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_anxiety_keyboard():
    keyboard = [
        ['🌬️ Дыхательные техники'],
        ['🌍 5-4-3-2-1'],
        ['💪 Физические техники'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_anxiety_techniques_keyboard(category: str):
    category_data = anxiety_techniques[category]
    techniques = [tech['name'] for tech in category_data['techniques']]
    
    keyboard = []
    row = []
    
    for technique in techniques:
        row.append(technique)
        if len(row) == 2:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append(['🔙 Назад'])
    
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_conflict_keyboard():
    keyboard = [
        ['🔄 Начать'],
        ['📋 Пример готовой фразы'], 
        ['💡 Что такое ННО?'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

'''def get_diary_keyboard():
    keyboard = [
        ['📝 Новая запись'],
        ['📚 Мои записи'],
        ['🔙 Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
'''