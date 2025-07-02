import telegram
from django.conf import settings

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

def send_telegram_message(chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
