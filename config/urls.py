from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView
from dotenv import load_dotenv
import os
from rest_framework_simplejwt.authentication import JWTAuthentication


load_dotenv()

schema_view = get_schema_view(
    openapi.Info(
        title="Habits Tracker API",
        default_version=os.getenv('PROJECT_VERSION'),
        description=os.getenv('PROJECT_DESCRIPTION'),
        authentication_classes=[JWTAuthentication],
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('habits.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', RedirectView.as_view(url='/swagger/', permanent=False)),
    path('auth/', include('users.urls')),
    path('telegram/', include('bot.urls')),
    path('', include('bot.urls')),
]