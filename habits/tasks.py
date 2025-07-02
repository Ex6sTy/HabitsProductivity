from celery import shared_task
from django.utils import timezone
from .models import Habit
from .telegram_utils import send_telegram_message


@shared_task
def test_celery():
    print("Celery работает!")
    return "SUCCESS"


@shared_task
def send_habit_reminders():
    now = timezone.now().time()
    habits = Habit.objects.filter(time__lte=now)
    for habit in habits:
        message = f"Напоминание: {habit.action} в {habit.time}"
        if habit.user.telegram_chat_id:
            send_telegram_message(habit.user.telegram_chat_id, message)

