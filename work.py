import asyncio
import logging
from telegram import Bot
from telegram.error import TelegramError

async def test_bot_connection(token: str):
    """Проверяет подключение к Telegram API"""
    try:
        bot = Bot(token=token)
        
        # Получаем информацию о боте
        bot_info = await bot.get_me()
        print(f"✅ Бот подключен успешно!")
        print(f"   Имя: @{bot_info.username}")
        print(f"   Название: {bot_info.first_name}")
        
        # Проверяем вебхук (если используется)
        webhook_info = await bot.get_webhook_info()
        print(f"   Вебхук: {webhook_info.url or 'Не установлен'}")
        
        return True
        
    except TelegramError as e:
        print(f"❌ Ошибка подключения к Telegram: {e}")
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка: {e}")
        return False

def load_config():
    """Загружает конфиг"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Ошибка загрузки config: {e}")
        return None

# Запуск проверки
async def main():
    config = load_config()
    if not config:
        return
    
    if 'BOT_TOKEN' in config:
        await test_bot_connection(config['BOT_TOKEN'])
    else:
        print("❌ BOT_TOKEN не найден в конфиге")

# Для запуска в синхронном коде
if __name__ == "__main__":
    asyncio.run(main())