from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(TestCase):

    def setUp(self):
        self.url = reverse('register')  # Replace with your registration URL

    def test_successful_registration(self):
        response = self.client.post(self.url, {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'securepassword123',
            'password2': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_registration_with_mismatched_passwords(self):
        response = self.client.post(self.url, {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'securepassword123',
            'password2': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)  # Assuming registration page reloads on error
        self.assertContains(response, "Passwords must match")



class UserLoginTest(TestCase):

    def setUp(self):
        self.login_url = reverse('login')  # Replace with your login URL
        self.user = User.objects.create_user(username='testuser', password='securepassword123')

    def test_successful_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'securepassword123'
        })
        self.assertEqual(response.status_code, 302)  # Assuming redirect after successful login
        self.assertTrue(self.client.login(username='testuser', password='securepassword123'))

    def test_unsuccessful_login(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Assuming login page reloads on error
        self.assertContains(response, "Invalid credentials")


class UserLogoutTest(TestCase):

    def setUp(self):
        self.logout_url = reverse('logout')  # Replace with your logout URL
        self.user = User.objects.create_user(username='testuser', password='securepassword123')
        self.client.login(username='testuser', password='securepassword123')

    def test_successful_logout(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Assuming redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)



class PasswordResetTest(TestCase):

    def setUp(self):
        self.email = 'testuser@example.com'
        self.user = User.objects.create_user(username='testuser', email=self.email, password='securepassword123')
        self.reset_url = reverse('password_reset')  # Replace with your password reset URL

    def test_successful_password_reset(self):
        response = self.client.post(self.reset_url, {'email': self.email})
        self.assertEqual(response.status_code, 302)  # Assuming redirect after successful request
        # Check for email sent (if your email backend is configured to use console for testing)
        # or check other aspects of the reset process
