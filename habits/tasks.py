from celery import shared_task
from .models import Habit
from django.utils import timezone
from bot.telegram_utils import send_telegram_message

@shared_task
def send_habit_reminders():
    now = timezone.now().time()
    habits = Habit.objects.filter(time__lte=now)

    for habit in habits:
        user = habit.user
        if user.telegram_id:
            message = f"🔔 Напоминание: пора заняться привычкой «{habit.title}»"
            send_telegram_message(user.telegram_id, message)

