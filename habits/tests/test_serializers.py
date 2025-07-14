from datetime import time

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from habits.models import Habit
from habits.serializers import HabitSerializer
from users.models import User


class HabitSerializerTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.context = {"request": self._mock_request()}

    def _mock_request(self):
        class Request:
            def __init__(self, user):
                self.user = user

        return Request(self.user)

    def test_valid_habit(self):
        data = {
            "place": "Home",
            "time": "12:00:00",
            "action": "Read book",
            "is_pleasant": False,
            "reward": "Chocolate",
            "duration": 60,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        habit = serializer.save()
        self.assertEqual(habit.user, self.user)

    def test_reward_and_related_habit_error(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Park",
            time=time(10, 0),
            action="Walk",
            is_pleasant=True,
            duration=60,
        )
        data = {
            "place": "Office",
            "time": "09:00:00",
            "action": "Check emails",
            "is_pleasant": False,
            "reward": "Coffee",
            "related_habit": pleasant.id,
            "duration": 30,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_duration_too_long_error(self):
        data = {
            "place": "Gym",
            "time": "07:00:00",
            "action": "Workout",
            "is_pleasant": False,
            "reward": "Smoothie",
            "duration": 300,
            "is_public": False,
        }
        serializer = HabitSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_pleasant_habit_with_reward_error(self):
        data = {
            "place": "Park",
            "time": "18:00:00",
            "action": "Jogging",
            "is_pleasant": True,
            "reward": "Dinner",
            "duration": 60,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_pleasant_habit_with_related_error(self):
        pleasant = Habit.objects.create(
            user=self.user,
            place="Lake",
            time=time(6, 0),
            action="Swim",
            is_pleasant=True,
            duration=30,
        )
        data = {
            "place": "Home",
            "time": "19:00:00",
            "action": "Meditate",
            "is_pleasant": True,
            "related_habit": pleasant.id,
            "duration": 60,
            "is_public": True,
        }
        serializer = HabitSerializer(data=data, context=self.context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
