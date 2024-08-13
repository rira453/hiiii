from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword'
        )

    def test_login_success(self):
        response = self.client.post(reverse('sing_in'), {'email': 'testuser@example.com', 'password': 'securepassword'})
        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('index'))

    def test_login_failure(self):
        response = self.client.post(reverse('sing_in'), {'email': 'testuser@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Mot de passe incorrect")

class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword'
        )

    def test_password_reset_request(self):
        response = self.client.post(reverse('forgot_password'), {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Un email a été envoyé avec les instructions pour réinitialiser votre mot de passe.")

       
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn('Modification de mot de passe!', email.subject)

    def test_password_reset_confirm(self):
        
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.post(reverse('update_password', kwargs={'uidb64': uid, 'token': token}), {
            'new_password': 'newsecurepassword',
            'confirm_password': 'newsecurepassword'
        })

        self.assertEqual(response.status_code, 302)  
        self.assertRedirects(response, reverse('sing_in'))

        # Tester la connexion avec un nouveau mot de passe
        response = self.client.post(reverse('sing_in'), {'email': 'testuser@example.com', 'password': 'newsecurepassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

class UserActivationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword',
            is_active=False  #L'utilisateur doit être inactif initialement
        )

    