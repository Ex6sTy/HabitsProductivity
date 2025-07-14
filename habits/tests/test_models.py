from datetime import time

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="pass123"
        )

    def test_str_representation_private(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time=time(8, 0),
            action="Чтение",
            duration=30,
            is_public=False,
        )
        self.assertEqual(str(habit), f"{self.user.email} — Чтение @ 08:00:00 (личная)")

    def test_str_representation_public(self):
        habit = Habit(
            user=self.user,
            place="Офис",
            time=time(9, 0),
            action="Планирование",
            duration=20,
            is_public=True,
        )
        self.assertEqual(
            str(habit), f"{self.user.email} — Планирование @ 09:00:00 (публичная)"
        )

    def test_clean_raises_if_reward_and_related_habit(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Кофейня",
            time=time(14, 0),
            action="Кофе",
            duration=10,
            is_pleasant=True,
        )
        habit = Habit(
            user=self.user,
            place="Офис",
            time=time(15, 0),
            action="Работа",
            duration=20,
            reward="Печенька",
            related_habit=pleasant,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_clean_raises_if_duration_too_long(self):
        habit = Habit(
            user=self.user,
            place="Дом",
            time=time(7, 0),
            action="Медитация",
            duration=121,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_clean_raises_if_pleasant_has_reward(self):
        habit = Habit(
            user=self.user,
            place="Квартира",
            time=time(10, 0),
            action="Релакс",
            duration=60,
            is_pleasant=True,
            reward="Шоколад",
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_clean_raises_if_pleasant_has_related_habit(self):
        related = Habit.objects.create(
            user=self.user,
            place="Парк",
            time=time(11, 0),
            action="Прогулка",
            duration=20,
            is_pleasant=True,
        )
        habit = Habit(
            user=self.user,
            place="Дача",
            time=time(12, 0),
            action="Работа в саду",
            duration=20,
            is_pleasant=True,
            related_habit=related,
        )
        with self.assertRaises(ValidationError):
            habit.clean()

    def test_clean_raises_if_frequency_too_large(self):
        habit = Habit(
            user=self.user,
            place="Офис",
            time=time(13, 0),
            action="Разбор задач",
            duration=25,
            frequency=8,
        )
        with self.assertRaises(ValidationError):
            habit.clean()
