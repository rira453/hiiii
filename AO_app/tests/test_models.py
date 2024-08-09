
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AO_app.models import *
from AO_app.forms import *
import re
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class ContactRequestModelTest(TestCase):

    def test_string_representation(self):
        contact_request = ContactRequest(full_name="John Doe")
        self.assertEqual(str(contact_request), contact_request.full_name)

    def test_verbose_name(self):
        self.assertEqual(ContactRequest._meta.verbose_name, "Demande de Contact")
        self.assertEqual(ContactRequest._meta.verbose_name_plural, "Demandes de Contact")

    def test_create_contact_request(self):
        contact_request = ContactRequest.objects.create(
            type_of_request="Demande d'info",
            company_name="Test Company",
            industry="Technology",
            full_name="John Doe",
            phone_number="0123456789",
            email="john@example.com",
            observations="Test observations"
        )
        self.assertEqual(contact_request.type_of_request, "Demande d'info")
        self.assertEqual(contact_request.company_name, "Test Company")
        self.assertEqual(contact_request.industry, "Technology")
        self.assertEqual(contact_request.full_name, "John Doe")
        self.assertEqual(contact_request.phone_number, "0123456789")
        self.assertEqual(contact_request.email, "john@example.com")
        self.assertEqual(contact_request.observations, "Test observations")



class ContactViewTest(TestCase):

    def test_contact_view_post_invalid_data(self):
        url = reverse('contact')
        data = {
            'type_of_request': "Demande d'info",
            'company_name': "Test Company",
            'industry': "Technology",
            'full_name': "John Doe",
            'phone_number': "0123456",  
            'email': "john@example.com",
            'observations': "Test observations"
        }
        response = self.client.post(url, data)
        
        if response.status_code == 302:  
            response = self.client.get(response.url)  
        self.assertEqual(response.status_code, 200)
        
        form = response.context.get('form')
        if form:
            self.assertFalse(form.is_valid())
            self.assertFormError(form, 'phone_number', "Veuillez entrer un numéro de téléphone marocain valide.")
        else:
            self.fail("Form not found in response context.")

    def test_contact_view_post_valid_data(self):
        url = reverse('contact')
        data = {
            'type_of_request': "Demande d'info",
            'company_name': "Test Company",
            'industry': "Technology",
            'full_name': "John Doe",
            'phone_number': "0612345678",  
            'email': "john@example.com",
            'observations': "Test observations"
        }
        response = self.client.post(url, data)
        
        if response.status_code == 302:  
            response = self.client.get(response.url)  
        self.assertEqual(response.status_code, 200)
        
        
        self.assertTrue(ContactRequest.objects.filter(full_name="John Doe").exists())


#  unit test  registration 
class UserRegistrationeTests(TestCase):
    
    def setUp(self):
        # Create a UserRegistratione instance for use in the tests
        self.user = UserRegistratione.objects.create(
            username='testuser',
            email='testuser@example.com',
            activite='Activity',
            categorie='Category',
            adresse='123 Street',
            ville='City',
            telephone='1234567890',
            fax='0987654321',
            password='securepassword'
        )
    
    def test_user_creation(self):
        # Check that the instance is created correctly
        self.assertEqual(UserRegistratione.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.activite, 'Activity')
        self.assertEqual(self.user.categorie, 'Category')
        self.assertEqual(self.user.adresse, '123 Street')
        self.assertEqual(self.user.ville, 'City')
        self.assertEqual(self.user.telephone, '1234567890')
        self.assertEqual(self.user.fax, '0987654321')
        self.assertEqual(self.user.password, 'securepassword')
    
    def test_string_representation(self):
        # Test the string representation of the instance
        self.assertEqual(str(self.user), 'testuser')

    def test_default_values(self):
        # Create a UserRegistratione instance with default values
        user_with_defaults = UserRegistratione.objects.create(
            username='defaultuser',
            email='defaultuser@example.com',
            password='defaultpassword'
        )
        self.assertEqual(user_with_defaults.categorie, 'Default Category')

    def test_verbose_name(self):
        # Check verbose name and plural name
        self.assertEqual(UserRegistratione._meta.verbose_name, "Inscription des utilisateurs")
        self.assertEqual(UserRegistratione._meta.verbose_name_plural, "Inscriptions des utilisateurs")

User = get_user_model()

