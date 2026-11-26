from datetime import timedelta

from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#2f7d5b")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return self.name


class CheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="checkins")
    date = models.DateField()

    class Meta:
        unique_together = ("habit", "date")
        ordering = ["-date"]


def compute_streaks(dates, today):
    """Return (current_streak, longest_streak) for a collection of dates.

    The current streak stays alive if you checked in yesterday but not yet today.
    """
    days = set(dates)
    one = timedelta(days=1)

    current = 0
    cursor = today if today in days else today - one
    while cursor in days:
        current += 1
        cursor -= one

    longest = run = 0
    prev = None
    for d in sorted(days):
        run = run + 1 if prev and d - prev == one else 1
        longest = max(longest, run)
        prev = d
    return current, longest
