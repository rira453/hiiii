from django.test import TestCase
from AO_app.models import *
from AO_app.forms import *
from django.test import TestCase
from django.core.exceptions import ValidationError

#Test contact request model
class ContactRequestModelTest(TestCase):

    def test_string_representation(self):
        contact_request = ContactRequest(full_name="Siham Idrissi")
        self.assertEqual(str(contact_request), contact_request.full_name)

    def test_verbose_name(self):
        self.assertEqual(ContactRequest._meta.verbose_name, "Demande de Contact")
        self.assertEqual(ContactRequest._meta.verbose_name_plural, "Demandes de Contact")

    def test_create_contact_request(self):
        contact_request = ContactRequest.objects.create(
            type_of_request="Demande d'info",
            company_name="Test Company",
            industry="Technology",
            full_name="Siham Idrissi",
            phone_number="0123456789",
            email="elidrissisiham@test.com",
            observations="Test observations"
        )
        self.assertEqual(contact_request.type_of_request, "Demande d'info")
        self.assertEqual(contact_request.company_name, "Test Company")
        self.assertEqual(contact_request.industry, "Technology")
        self.assertEqual(contact_request.full_name, "Siham Idrissi")
        self.assertEqual(contact_request.phone_number, "0123456789")
        self.assertEqual(contact_request.email, "elidrissisiham@test.com")
        self.assertEqual(contact_request.observations, "Test observations")

    def test_invalid_instance(self):
        instance = ContactRequest(
            type_of_request='Invalid Type',  
            observations=''  
        )
        with self.assertRaises(ValidationError) as context:
            instance.full_clean()

        self.assertIn('type_of_request', context.exception.error_dict)
        self.assertIn('observations', context.exception.error_dict)

    def test_string_representation(self):
        instance = ContactRequest(full_name='Siham Idrissi')
        self.assertEqual(str(instance), 'Siham Idrissi')




#table data model 
class TableDataTest(TestCase):
    def test_valid_instance(self):
        instance = TableData.objects.create(
            site='Test Site',
            numero_ao='12345',
            designation='Test Designation',
            categorie='Test Category',
            date_lancement='2024-01-01',
            date_remise='2024-01-10',
            date_ouverture='2024-01-15',
            estimation_projet_dhht=10000.00,
            seance_ouverture='Test Seance',
            pdf_file=None
        )
        self.assertIsInstance(instance, TableData)
        self.assertEqual(instance.numero_ao, '12345')

    def test_string_representation(self):
        instance = TableData(numero_ao='12345')
        self.assertEqual(str(instance), '12345')

    

#Marche model 

class MarcheTest(TestCase):
    def test_valid_instance(self):
        instance = Marche.objects.create(
            site='Test Site',
            numero_ao='67890',
            designation='Test Marche',
            categorie='Test Category',
            ouverture_financiere='2024-02-01',
            montant_dhht=20000.00,
            attributaire='Test Attributaire',
            detail='Test Detail'
        )
        self.assertIsInstance(instance, Marche)
        self.assertEqual(instance.numero_ao, '67890')

    def test_string_representation(self):
        instance = Marche(numero_ao='67890')
        self.assertEqual(str(instance), '67890')



#mise a jour mode
class NewsletterSubscriptionTest(TestCase):
    def test_valid_instance(self):
        instance = NewsletterSubscription.objects.create(
            email='test@example.com'
        )
        self.assertIsInstance(instance, NewsletterSubscription)
        self.assertEqual(instance.email, 'test@example.com')

    def test_string_representation(self):
        instance = NewsletterSubscription(email='test@example.com')
        self.assertEqual(str(instance), 'test@example.com')



#download history model
class DownloadHistoryTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.table_data = TableData.objects.create(
            site='Test Site',
            numero_ao='12345',
            designation='Test Designation',
            categorie='Test Category',
            date_lancement='2024-01-01',
            date_remise='2024-01-10',
            date_ouverture='2024-01-15',
            estimation_projet_dhht=10000.00,
            seance_ouverture='Test Seance',
            pdf_file=None
        )

    def test_valid_instance(self):
        instance = DownloadHistory.objects.create(
            user=self.user,
            table_data=self.table_data
        )
        self.assertIsInstance(instance, DownloadHistory)
        self.assertEqual(instance.user, self.user)

    def test_string_representation(self):
        instance = DownloadHistory(user=self.user, table_data=self.table_data)
        self.assertIn('downloaded', str(instance))

#Forms

class ContactFormTestCase(TestCase):
    
    def test_valid_form(self):
        data = {
            'type_of_request': 'Demande d\'info',
            'company_name': 'Test Company',
            'industry': 'Tech',
            'full_name': 'Siham Idrissi',
            'phone_number': '0612345678',
            'email': 'elidrissisiham@test.com',
            'observations': 'No observations'
        }
        form = ContactForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_phone_number(self):
        data = {
            'type_of_request': 'Demande d\'info',
            'company_name': 'Test Company',
            'industry': 'Tech',
            'full_name': 'Siham Idrissi',
            'phone_number': '123456789',
            'email': 'elidrissisiham@test.com',
            'observations': 'No observations'
        }
        form = ContactForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['phone_number'], ['Veuillez entrer un numéro de téléphone marocain valide.'])


class NewsletterFormTestCase(TestCase):

    def test_valid_email(self):
        data = {'email': 'valid.email@example.com'}
        form = NewsletterForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
     data = {'email': 'invalid-email'}
     form = NewsletterForm(data=data)
     self.assertFalse(form.is_valid())
     # Check against the localized error message
     self.assertEqual(form.errors['email'], ['Saisissez une adresse de courriel valide.'])



class RegistrationFormTestCase(TestCase):

    def test_valid_form(self):
     data = {
        'username': 'SihamIdrissi',
        'email': 'elidrissisiham@test.com',
        'password1': 'StrongP@ssw0rd!',
        'password2': 'StrongP@ssw0rd!',
        'activite': 'Developer',
        'categorie': 'Category',
        'adresse': '123 Street',
        'ville': 'City',
        'telephone': '0612345678',
        'fax': '0612345678'
    }
     form = RegistrationForm(data=data)
     self.assertTrue(form.is_valid(), "Form should be valid, but it's not.")

    
    def test_duplicate_email(self):
        User.objects.create_user(username='existinguser', email='elidrissisiham@test.com', password='password123')
        data = {
            'username': 'newuser',
            'email': 'elidrissisiham@test.com',
            'password1': 'password123',
            'password2': 'password123',
            'activite': 'Developer',
            'categorie': 'Category',
            'adresse': '123 Street',
            'ville': 'City',
            'telephone': '0612345678',
            'fax': '0612345678'
        }
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['An account with this email address already exists!'])



