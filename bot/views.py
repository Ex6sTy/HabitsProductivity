import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from django.conf import settings
import requests


@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            message = data.get("message", {})
            chat = message.get("chat", {})
            chat_id = chat.get("id")
            text = message.get("text", "")

            if not chat_id:
                return JsonResponse({"ok": False, "error": "No chat_id"}, status=400)

            # Привязываем Telegram chat_id к email
            user, created = User.objects.get_or_create(email=f"{chat_id}@example.com")
            user.telegram_id = chat_id
            user.save()

            # Ответ на команду /start
            if text.strip().lower() == "/start":
                reply = "Привет! ✅ Ты успешно подписался на напоминания. Мы будем сообщать тебе о твоих привычках."
                requests.post(
                    f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
                    json={"chat_id": chat_id, "text": reply}
                )

            return JsonResponse({"ok": True})

        except Exception as e:
            return JsonResponse({"ok": False, "error": str(e)}, status=500)

    return JsonResponse({"ok": True})
