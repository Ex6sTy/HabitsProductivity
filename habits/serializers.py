from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            "id",
            "user",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "reward",
            "duration",
            "is_public",
            "created_at",
        ]
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        instance = Habit(user=self.context["request"].user, **attrs)
        try:
            instance.clean()
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                e.message_dict
                if hasattr(e, "message_dict")
                else {"non_field_errors": e.messages}
            )
        return attrs

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
