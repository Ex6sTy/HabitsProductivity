# habits/tests/test_permissions.py
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from habits.models import Habit
from habits.permissions import IsOwnerOrReadOnly
from habits.views import HabitViewSet
from users.models import User


class IsOwnerOrReadOnlyTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email="owner@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="notowner@example.com", password="testpass123"
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Park",
            time="08:00",
            action="Run",
            is_pleasant=False,
            frequency=1,
            duration=60,
            is_public=False,
        )
        self.permission = IsOwnerOrReadOnly()

    def test_owner_has_permission(self):
        request = self.factory.get("/api/habits/")
        request.user = self.user
        view = HabitViewSet()
        self.assertTrue(
            self.permission.has_object_permission(request, view, self.habit)
        )

    def test_not_owner_no_permission(self):
        request = self.factory.get("/api/habits/")
        request.user = self.other_user
        view = HabitViewSet()
        self.assertFalse(
            self.permission.has_object_permission(request, view, self.habit)
        )
