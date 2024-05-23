from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthenticationTest(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            username=self.username, password=self.password)

    def test_user_signup(self):
        signup_url = reverse('users:signup')
        new_username = 'newuser'
        new_password = 'newpassword'
        response = self.client.post(
            signup_url, {'username': new_username, 'password': new_password})
        self.assertEqual(response.status_code, 200)

    def test_user_login_valid(self):
        login_url = reverse('users:login')
        response = self.client.post(
            login_url, {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)

    def test_user_login_wrong(self):
        login_url = reverse('users:login')
        response = self.client.post(
            login_url, {'username': 'qwerty', 'password': 'qwerty123'})
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        logout_url = reverse('users:logout')
        response = self.client.get(logout_url)
        self.assertEqual(response.status_code, 200)

