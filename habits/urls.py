from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HabitViewSet
from django.http import JsonResponse


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health_check),
    path('', include(router.urls)),
]
