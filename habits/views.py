from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CheckIn, Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).prefetch_related("checkins")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def toggle(self, request, pk=None):
        """Check in for a day (default today); calling it again un-checks it."""
        habit = self.get_object()
        day = parse_date(request.data.get("date") or "") or timezone.localdate()
        if day > timezone.localdate():
            return Response({"detail": "Can't check in for a future date."}, status=400)
        obj, created = CheckIn.objects.get_or_create(habit=habit, date=day)
        if not created:
            obj.delete()
        return Response(self.get_serializer(self.get_queryset().get(pk=pk)).data)


@api_view(["GET"])
def stats(request):
    """Daily completion rate for the last N days (default 14)."""
    days = max(1, min(int(request.query_params.get("days", 14)), 90))
    today = timezone.localdate()
    start = today - timedelta(days=days - 1)
    total = Habit.objects.filter(user=request.user).count()
    rows = (CheckIn.objects.filter(habit__user=request.user, date__gte=start)
            .values("date").annotate(n=Count("id")))
    done = {r["date"]: r["n"] for r in rows}
    data = []
    for i in range(days):
        d = start + timedelta(days=i)
        n = done.get(d, 0)
        data.append({"date": str(d), "label": d.strftime("%d %b"), "completed": n,
                     "percent": round(100 * n / total) if total else 0})
    return Response(data)


def _auth_response(user):
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key, "username": user.username})


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = (request.data.get("username") or "").strip()
    password = request.data.get("password") or ""
    if not username or len(password) < 6:
        return Response({"detail": "Enter a username and a password of at least 6 characters."}, status=400)
    if User.objects.filter(username__iexact=username).exists():
        return Response({"detail": "That username is taken."}, status=400)
    return _auth_response(User.objects.create_user(username=username, password=password))


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
    if not user:
        return Response({"detail": "Wrong username or password."}, status=status.HTTP_400_BAD_REQUEST)
    return _auth_response(user)
