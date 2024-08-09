from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from AO_app.models import *



class PasswordResetTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='securepassword123')
        self.reset_url = reverse('forgot_password')
        self.update_password_url = reverse('update_password', kwargs={'uidb64': 'dummyuid', 'token': 'dummytoken'})
    
    def test_password_reset_request(self):
        response = self.client.post(self.reset_url, {'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)  # Check if request is processed
        self.assertEqual(len(mail.outbox), 1)  # Check if password reset email is sent

    def test_password_update(self):
        # Simulate a valid password reset flow
        response = self.client.post(self.update_password_url, {'new_password': 'newpassword123', 'confirm_password': 'newpassword123'})
        self.assertEqual(response.status_code, 302)  # Should redirect after password update
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))


class FileDownloadTests(TestCase):

    def setUp(self):
        self.table_data = TableData.objects.create(
            site='Test Site',
            numero_ao='12345',
            designation='Test Designation',
            categorie='Test Category',
            date_lancement='2024-01-01',
            date_remise='2024-01-02',
            date_ouverture='2024-01-03',
            estimation_projet_dhht=10000,
            seance_ouverture='Test Seance',
            pdf_file='path/to/file.pdf'
        )
        self.download_url = reverse('download_pdf', args=[self.table_data.pk])

    def test_file_download(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.table_data.pdf_file.name}"')
