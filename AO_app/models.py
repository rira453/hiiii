from django.db import models

from .encryption import encrypt, decrypt, generate_key
import os

from django.contrib.auth.models import User
class ContactRequest(models.Model):
    TYPE_OF_REQUEST_CHOICES = [
        ('Demande d\'info', 'Demande d\'info'),
        ('Reclamation', 'Reclamation'),
        ('Reclamation anonyme', 'Reclamation anonyme')
    ]
    
    type_of_request = models.CharField(max_length=50, choices=TYPE_OF_REQUEST_CHOICES)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()
    observations = models.TextField()
    
    def __str__(self):
        return self.full_name

    
class TableData(models.Model):
    site = models.CharField(max_length=100)
    numero_ao = models.CharField(max_length=100)
    designation = models.TextField()
    categorie = models.TextField()
    date_lancement = models.DateField()
    date_remise = models.DateField()
    date_ouverture = models.DateField()
    estimation_projet_dhht = models.FloatField()
    seance_ouverture = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    

    def __str__(self):
        return self.numero_ao
    
class Marche(models.Model):
    site = models.CharField(max_length=100)
    numero_ao = models.CharField(max_length=100)
    designation = models.TextField()
    categorie = models.TextField()
    ouverture_financiere = models.DateField()
    montant_dhht = models.DecimalField(max_digits=10, decimal_places=2)
    attributaire = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return self.numero_ao
    
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)  # Updated to EmailField
    
    def __str__(self):
        return self.user.username
    
class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_data = models.ForeignKey(TableData, on_delete=models.CASCADE)
    download_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.table_data.numero_ao} on {self.download_timestamp}"
    
class UserRegistratione(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    activite = models.CharField(max_length=150, blank=True)
    categorie= models.CharField(max_length=150, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=128)  # Store plain password temporarily

    def __str__(self):
        return self.username
    




KEY = os.getenv('ENCRYPTION_KEY')
SALT = os.getenv('ENCRYPTION_SALT')

if not KEY or not SALT:
    raise ValueError("Les variables d'environnement ENCRYPTION_KEY et ENCRYPTION_SALT doivent être définies.")

class SensitiveData(models.Model):
    encrypted_field = models.BinaryField()

    def save(self, *args, **kwargs):
        # Encrypt the data before saving
        self.encrypted_field = encrypt(self.encrypted_field, KEY)
        super().save(*args, **kwargs)

    def decrypt_data(self):
        return decrypt(self.encrypted_field, KEY)



