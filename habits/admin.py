from django.contrib import admin

from .models import CheckIn, Habit

admin.site.register(Habit)
admin.site.register(CheckIn)
