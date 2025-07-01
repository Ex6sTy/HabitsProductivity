from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = [
            'id',
            'user',
            'place',
            'time',
            'action',
            'is_pleasant',
            'related_habit',
            'periodicity',
            'reward',
            'duration',
            'is_public',
            'created_at',
        ]
        read_only_fields = ['user', 'created_at']

    def validate(self, data):
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError("Укажите либо вознаграждение, либо связанную привычку, не оба поля.")

        if data.get('duration', 0) > 120:
            raise serializers.ValidationError("Привычка не должна выполняться дольше 120 секунд.")

        if data.get('is_pleasant') and (data.get('reward') or data.get('related_habit')):
            raise serializers.ValidationError("Приятная привычка не может иметь вознаграждение или связанную привычку.")

        if 'periodicity' in data and (data['periodicity'] < 1 or data['periodicity'] > 7):
            raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")

        return data
