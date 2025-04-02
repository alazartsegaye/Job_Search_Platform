from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import User

class UserViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.home_url = reverse('home')
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('user-profile')
        
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "password": "TestPass123!"
        }
        
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            email=self.user_data['email'],
            password=self.user_data['password']
        )
        self.token = Token.objects.create(user=self.user)
        
    def test_home_view(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "email": "newuser@example.com",
            "password": "NewPass123!"
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_view_success(self):
        response = self.client.post(self.home_url, {
            'username': 'testuser',
            'password': 'TestPass123!'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_view_invalid(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid credentials')

    def test_logout_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(self.home_url, follow=True)
        
        self.assertEqual(response.status_code, 200)

    def test_user_profile_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('username'), 'testuser')
