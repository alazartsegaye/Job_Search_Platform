from django.test import TestCase, Client
from users.models import User
from django.urls import reverse
from users.forms import RegisterForm
from users.views import UserProfileView
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework import status
from django.contrib.messages import get_messages
from rest_framework.authtoken.models import Token

class UserViewsTest(TestCase):
    # Test Case for user-related views (home, login, registration)
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            password='password123', 
            email='admin@example.com'
        )
        self.regular_user = User.objects.create_user(
            username='user', 
            password='password123', 
            email='user@example.com'
        )
        self.client = Client()
        self.home_url = reverse('home')
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.profile_url = reverse('user-profile')

    def test_home_view(self):
        # Test that the home view loads successfully and uses the correct template
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/home.html')

    def test_login_view_success(self):
        # Test successful login and token generation for a valid user
        self.user_data = {
            "username": "testuser",
            "password": "testpass123"
        }
        user = User.objects.create_user(**self.user_data)
        Token.objects.create(user=user)

        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_login_view_invalid(self):
        # Test login failure with invalid credentials
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get('error'), 'Invalid credentials')

    def test_register_view_get(self):
        # Test that the registration view loads successfully with the correct form
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegisterForm)

    def test_register_view_success(self):
        # Test successful registration and user creation
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User ',
            'email': 'new@example.com',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

        token = Token.objects.get(user__username='newuser')
        self.assertTrue(token.key) 

    def test_register_view_invalid_data(self):
        # Test registration failure with invalid data
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User ',
            'email': 'invalid-email',
            'password1': 'complexpassword123',
            'password2': 'differentpassword'
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='newuser').exists())
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue("Registration failed" in str(messages[0]))

class UserProfileViewTest(TestCase):
    # Test suite for user profile view functionality
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile_url = reverse('user-profile')

    def test_user_profile_view_authenticated(self):
        # Test that authenticated users can access their profile
        request = self.factory.get(self.profile_url)
        request.user = self.user
        response = UserProfileView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_profile_view_unauthenticated(self):
        # Test that unauthenticated users are denied access to the profile
        response = self.client.get(self.profile_url)    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

class UserPermissionsTest(TestCase):
    # Test case for user permissions related to accessing the user list
    def setUp(self):
        # Create an admin user and a regular user for testing permissions
        self.admin = User.objects.create_superuser(
            username='admin',
            password='adminpass'
        )
        self.user = User.objects.create_user(
            username='regular',
            password='regularpass'
        )
        self.client = APIClient()
        self.users_url = reverse('user-list')

    def test_admin_can_list_users(self):
        # Test that an admin user can successfully access the user list
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_list_users(self):
        # Test that a regular user is denied access to the user list
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)