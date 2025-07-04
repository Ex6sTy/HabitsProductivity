from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits'
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_pleasant': True},
        related_name='related_to'
    )
    periodicity = models.PositiveSmallIntegerField(default=1)  # в днях
    reward = models.CharField(max_length=255, blank=True, null=True)
    duration = models.PositiveIntegerField(help_text="Время в секундах")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def clean(self):
        super().clean()

        if self.reward and self.related_habit:
            raise ValidationError("Нельзя одновременно указать вознаграждение и связанную привычку.")

        if self.duration > 120:
            raise ValidationError("Привычка не должна выполняться дольше 120 секунд.")

        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError("Приятная привычка не может иметь ни вознаграждение, ни связанную привычку.")

        if not 1 <= self.periodicity <= 7:
            raise ValidationError("Нельзя выполнять привычку реже одного раза в 7 дней.")

    def __str__(self):
        visibility = 'публичная' if self.is_public else 'личная'
        return f"{self.user.email} — {self.action} @ {self.time} ({visibility})"
