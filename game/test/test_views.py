from django.test import TestCase
from django.urls import reverse
# from django.test.client import Client
from django.contrib.auth.models import User
# from game.models import Location, Profile, Announcement, Safezone

class RegistrationTests(TestCase):
    pass

class IndexViewTests(TestCase):
    """Testing index view"""
    def test_index_view_exists(self):
        """Test view works"""
        response = self.client.get(reverse('game:index'))
        self.assertEqual(response.status_code, 200)

class LoginTestCase(TestCase):
    """Testing Login Views"""
    def test_login_view_exists(self):
        """Login view exists"""
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_works(self):
        """User is authenticated after logging in"""
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        self.client.login(username='username', password='password')
        self.assertEqual(test_user.is_authenticated, True)

#    def test_redirects_to_home_page(self):
#        response = self.client.post('/login/', data={
#            'username': 'username', 'password': 'password'
#        })
#        self.assertRedirects(response, '/game/play')

class LogoutViewTests(TestCase):
    """Testing register view"""
    def test_register_view_exists(self):
        """Test view works"""
        response = self.client.get(reverse('game:logout_successful'))
        self.assertEqual(response.status_code, 200)

class UserViewTests(TestCase):
    """Testing users view"""
    def test_users_view_exists(self):
        """Test view exists"""
        response = self.client.get(reverse('game:users'))
        self.assertEqual(response.status_code, 200)

class UserProfileViewTests(TestCase):
    """Test viewing of user profile"""
    def test__view_when_logged_in(self):
        """Test logged in user can access view"""
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('game:user_detail'))
        self.assertEqual(response.status_code, 200)

    def test_view_when_not_logged_in(self):
        """Test view cannot be accessed"""
        response = self.client.get(reverse('game:user_detail'))
        self.assertEqual(response.status_code, 302)

class LeaderboardViewTests(TestCase):
    """Testing leaderboard view"""
    def test_leaderboard_view_exists(self):
        """Test view exists"""
        response = self.client.get(reverse('game:leaderboard'))
        self.assertEqual(response.status_code, 200)

    def test_ranking(self):
        """Test ranking variable returns user"""
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        test_user.profile.matches_won = 30
        test_user.profile.matches_lost = 20
        test_user.profile.save()
        response = self.client.get(reverse('game:leaderboard'))

        ranking = response.context['ranking']
        get_users = response.context['get_users']
        result = list(get_users)
        for i in result:
            user_name = i.user
            user_name = user_name.username
        self.assertEqual(user_name, 'username')

        rates = response.context['rates']
        self.assertEqual(rates, [60.0])
        matches = response.context['matches']
        self.assertEqual(matches, [50])

        self.assertEqual(ranking, [(test_user.username, test_user.profile.success_rate(), int(test_user.profile.total_matches()))])

    def test_ranking_with_multiple_users(self):
        """Test ranking variable returns user"""
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        test_user.profile.matches_won = 10
        test_user.profile.matches_lost = 30
        test_user.profile.save()
        test_user = User.objects.create_user('user',
                                             'user@example.com', 'password')
        test_user.profile.matches_won = 30
        test_user.profile.matches_lost = 20
        test_user.profile.save()
        test_user = User.objects.create_user('user1',
                                             'user@example.com', 'password')
        test_user.profile.matches_won = 40
        test_user.profile.matches_lost = 10
        test_user.profile.save()
        response = self.client.get(reverse('game:leaderboard'))

        ranking = response.context['ranking']
        self.assertEqual(ranking, [('user1', 80.0, 50), ('user', 60.0, 50), ('username', 25.0, 40)])

class PlayViewTests(TestCase):
    """Testing play view"""
    def test_play_view_exists(self):
        """Test view exists"""
        response = self.client.get(reverse('game:play'))
        self.assertEqual(response.status_code, 200)

    def test_play_view_data_retrieval_no_user(self):
        response = self.client.get(reverse('game:play'))
        self.assertEqual(response.context['antidotes'],
                         "Please log in to save your progress!")

    def test_play_view_data_retrieval_with_no_antidote(self):
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('game:play'))
        self.assertEqual(response.context['antidotes'], test_user.profile.num_antidotes)

    def test_play_view_data_retrieval_with_two_antidotes(self):
        test_user = User.objects.create_user('username',
                                             'user@example.com', 'password')
        self.client.login(username='username', password='password')
        test_user.profile.num_antidotes = 2
        test_user.profile.save()
        response = self.client.get(reverse('game:play'))
        self.assertEqual(response.context['antidotes'], test_user.profile.num_antidotes)
