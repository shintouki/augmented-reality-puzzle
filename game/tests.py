import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from game.models import Location, Profile

def create_user(username):
    pass

class IndexViewTests(TestCase):
    def test_index_view_exists(self):
        response = self.client.get(reverse('game:index'))
        self.assertEqual(response.status_code, 200)

class RegisterViewTests(TestCase):
    def test_register_view_exists(self):
        pass

class UserViewTests(TestCase):
    def test_users_view_exists(self):
        response = self.client.get(reverse('game:users'))
        self.assertEqual(response.status_code, 200)

    def test_users_view_with_no_users(self):
        pass

    def test_users_view_with_one_user(self):
        pass

    def test_users_view_with_two_users(self):
        pass

    def test_users_view_with_multiple_users(self):
        pass

class LeaderboardViewTests(TestCase):
    def test_leaderboard_view_exists(self):
        response = self.client.get(reverse('game:leaderboard'))
        self.assertEqual(response.status_code, 200)

class RegistrationTests(TestCase):
    pass

class LocationTestCase(TestCase):

    # create test location
    def create_locations(location_text, matches_won, matches_lost):
        return Location.objects.create(location_text=location_text, matches_won=matches_won, matches_lost=matches_lost)

    # test location field values
    def test_locationfields(self):
        ccny = Location.objects.create(location_text="CCNY")
        shepard = Location.objects.create(location_text="Shepard", matches_won=10, matches_lost=10)
        shepard_name = "Shepard"
        self.assertEqual(ccny.matches_won, 70)
        self.assertEqual(shepard.matches_lost, 10)
        self.assertNotEqual(shepard.matches_lost, 20)
        self.assertEqual(shepard.location_text, shepard_name)

    # test total matches method
    def test_total_methods(self):
        ccny = Location.objects.create(location_text="CCNY")
        self.assertEqual(ccny.total_matches(), 100)

    # test infection rate method
    def test_infection_rate(self):
        ccny = Location.objects.create(location_text="CCNY")
        self.assertEqual(ccny.infection_rate(), 30)
