from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Habit
from .serializers import HabitSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and obj.is_public:
            return True
        return obj.user == request.user


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['created_at', 'time']
    ordering = ['-created_at']
    search_fields = ['action', 'place']

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(Q(user=user) | Q(is_public=True))

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=False,
        methods=['get'],
        url_path='public',
        permission_classes=[permissions.AllowAny]
    )
    def public(self, request):
        queryset = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

