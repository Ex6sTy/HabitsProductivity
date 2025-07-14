from datetime import time

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", password="testpass123"
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time=time(12, 0),
            action="Test Habit",
            is_pleasant=False,
            frequency=1,
            duration=60,
            is_public=False,
        )

        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Park",
            time=time(14, 0),
            action="Public Habit",
            is_pleasant=True,
            frequency=1,
            duration=30,
            is_public=True,
        )

        self.client.login(email="user@example.com", password="testpass123")

    def test_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")
        data = {
            "place": "Gym",
            "time": "08:00:00",
            "action": "Workout",
            "is_pleasant": False,
            "frequency": 1,
            "duration": 60,
            "is_public": True,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

    def test_retrieve_own_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_habit_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=[self.public_habit.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_habits(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=[self.habit.id])
        data = {
            "place": "Updated Place",
            "time": "10:00:00",
            "action": "Updated Action",
            "is_pleasant": False,
            "frequency": 2,
            "duration": 50,
            "is_public": False,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, "Updated Place")

    def test_delete_habit(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_list_public_habits(self):
        url = reverse("habits:habit-public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertIn(self.public_habit.id, [h["id"] for h in results])
