from datetime import time, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from habits.models import Habit
from habits.tasks import send_habit_reminders
from users.models import User


class SendHabitRemindersTaskTest(TestCase):
    def setUp(self):
        self.user_with_telegram = User.objects.create_user(
            email="user1@example.com", password="testpass", telegram_id="123456"
        )
        self.user_without_telegram = User.objects.create_user(
            email="user2@example.com", password="testpass"
        )

        now = timezone.now().time()

        self.habit1 = Habit.objects.create(
            user=self.user_with_telegram,
            place="Дом",
            time=now,
            action="Чтение",
            is_pleasant=False,
            duration=60,
            is_public=True,
        )

        self.habit2 = Habit.objects.create(
            user=self.user_without_telegram,
            place="Офис",
            time=now,
            action="Медитация",
            is_pleasant=False,
            duration=90,
            is_public=False,
        )

    @patch("habits.tasks.send_telegram_message")
    def test_send_habit_reminders_sends_message_to_valid_users(self, mock_send_message):
        send_habit_reminders()

        mock_send_message.assert_called_once_with(
            self.user_with_telegram.telegram_id,
            f"🔔 Напоминание: пора заняться привычкой «{self.habit1.action}»",
        )
