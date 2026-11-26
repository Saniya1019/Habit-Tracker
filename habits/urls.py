from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("habits", views.HabitViewSet, basename="habit")

urlpatterns = [
    path("register/", views.register),
    path("login/", views.login),
    path("stats/", views.stats),
    path("", include(router.urls)),
]
