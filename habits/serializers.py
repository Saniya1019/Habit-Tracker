from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Habit, compute_streaks


class HabitSerializer(serializers.ModelSerializer):
    current_streak = serializers.SerializerMethodField()
    longest_streak = serializers.SerializerMethodField()
    checked_today = serializers.SerializerMethodField()
    total_checkins = serializers.SerializerMethodField()
    last_7_days = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = ["id", "name", "color", "current_streak", "longest_streak",
                  "checked_today", "total_checkins", "last_7_days"]

    def _dates(self, obj):
        return {c.date for c in obj.checkins.all()}

    def get_current_streak(self, obj):
        return compute_streaks(self._dates(obj), timezone.localdate())[0]

    def get_longest_streak(self, obj):
        return compute_streaks(self._dates(obj), timezone.localdate())[1]

    def get_checked_today(self, obj):
        return timezone.localdate() in self._dates(obj)

    def get_total_checkins(self, obj):
        return len(self._dates(obj))

    def get_last_7_days(self, obj):
        today, dates = timezone.localdate(), self._dates(obj)
        return [{"date": str(d), "done": d in dates}
                for d in (today - timedelta(days=i) for i in range(6, -1, -1))]
