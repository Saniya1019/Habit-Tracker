from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from .models import compute_streaks

T = date(2025, 1, 10)
D = lambda n: T - timedelta(days=n)


class StreakTests(TestCase):
    def test_empty(self):
        self.assertEqual(compute_streaks([], T), (0, 0))

    def test_current_includes_today(self):
        self.assertEqual(compute_streaks([D(0), D(1), D(2)], T), (3, 3))

    def test_streak_alive_if_only_yesterday(self):
        self.assertEqual(compute_streaks([D(1), D(2)], T), (2, 2))

    def test_streak_broken(self):
        self.assertEqual(compute_streaks([D(2), D(3), D(4)], T), (0, 3))

    def test_longest_differs_from_current(self):
        self.assertEqual(compute_streaks([D(0), D(5), D(6), D(7), D(8)], T), (1, 4))


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        res = self.client.post("/api/register/", {"username": "sam", "password": "secret123"})
        self.client.credentials(HTTP_AUTHORIZATION="Token " + res.data["token"])

    def test_create_and_toggle(self):
        hid = self.client.post("/api/habits/", {"name": "Read"}).data["id"]
        r = self.client.post(f"/api/habits/{hid}/toggle/")
        self.assertTrue(r.data["checked_today"])
        self.assertEqual(r.data["current_streak"], 1)
        r = self.client.post(f"/api/habits/{hid}/toggle/")
        self.assertFalse(r.data["checked_today"])

    def test_users_are_isolated(self):
        self.client.post("/api/habits/", {"name": "Read"})
        other = APIClient()
        tok = other.post("/api/register/", {"username": "alex", "password": "secret123"}).data["token"]
        other.credentials(HTTP_AUTHORIZATION="Token " + tok)
        self.assertEqual(len(other.get("/api/habits/").data), 0)

    def test_no_future_checkin(self):
        hid = self.client.post("/api/habits/", {"name": "Run"}).data["id"]
        tomorrow = str(timezone.localdate() + timedelta(days=1))
        self.assertEqual(self.client.post(f"/api/habits/{hid}/toggle/", {"date": tomorrow}).status_code, 400)

    def test_stats(self):
        hid = self.client.post("/api/habits/", {"name": "Run"}).data["id"]
        self.client.post(f"/api/habits/{hid}/toggle/")
        data = self.client.get("/api/stats/?days=7").data
        self.assertEqual(len(data), 7)
        self.assertEqual(data[-1]["percent"], 100)
