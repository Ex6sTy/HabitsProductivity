from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import HabitViewSet


router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok"})


urlpatterns = [
    path('health/', health_check),
    path('', include(router.urls)),
]
