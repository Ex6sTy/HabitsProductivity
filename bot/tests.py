import json
from unittest.mock import patch

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from users.models import User


class TelegramWebhookTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("telegram_webhook")
        self.chat_id = "123456"
        self.start_message = {
            "message": {"chat": {"id": self.chat_id}, "text": "/start"}
        }

    @patch("requests.post")
    def test_start_command_creates_user_and_sends_reply(self, mock_post):
        response = self.client.post(
            self.url,
            data=json.dumps(self.start_message),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            User.objects.filter(email=f"{self.chat_id}@example.com").exists()
        )

        user = User.objects.get(email=f"{self.chat_id}@example.com")
        self.assertEqual(user.telegram_id, self.chat_id)

        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={
                "chat_id": self.chat_id,
                "text": "Привет! ✅ Ты успешно подписался на напоминания. Мы будем сообщать тебе о твоих привычках.",
            },
        )

    def test_missing_chat_id_returns_error(self):
        payload = {"message": {"chat": {}, "text": "/start"}}

        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_non_post_returns_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ok": True})


class SendTelegramMessageTests(TestCase):
    @patch("requests.post")
    def test_send_telegram_message_posts_to_api(self, mock_post):
        from bot.telegram_utils import send_telegram_message

        chat_id = "123456"
        text = "Hello, World!"

        send_telegram_message(chat_id, text)

        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text},
        )
