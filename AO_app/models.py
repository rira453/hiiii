from django.db import models


import os

from django.contrib.auth.models import User
class ContactRequest(models.Model):
    TYPE_OF_REQUEST_CHOICES = [
        ('Demande d\'info', 'Demande d\'info'),
        ('Reclamation', 'Reclamation'),
        ('Reclamation anonyme', 'Reclamation anonyme')
    ]
    
    
    type_of_request = models.CharField(max_length=50, choices=TYPE_OF_REQUEST_CHOICES,verbose_name='Type de demande')
    company_name = models.CharField(max_length=255, null=True,blank=True, verbose_name="Nom de l'entreprise")
    industry = models.CharField(max_length=255, null=True,blank=True, verbose_name="Secteur d'activité")
    full_name = models.CharField(max_length=255, null=True,blank=True, verbose_name="Nom complet")
    phone_number = models.CharField(max_length=15, null=True,blank=True, verbose_name="Numéro de téléphone")
    email = models.EmailField(null=True,blank=True,)
    observations = models.TextField()
    
    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Demande de Contact"  # Singular display name
        verbose_name_plural = "Demandes de Contact"  # Plural display name

    
class TableData(models.Model):
    site = models.CharField(max_length=100)
    numero_ao = models.CharField(max_length=100)
    designation = models.TextField()
    categorie = models.TextField(default='Default Category')
    date_lancement = models.DateField()
    date_remise = models.DateField()
    date_ouverture = models.DateField()
    estimation_projet_dhht = models.FloatField()
    seance_ouverture = models.CharField(max_length=100)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    

    def __str__(self):
        return self.numero_ao
    
    class Meta:
        verbose_name = "Table AO"  # Singular display name
        verbose_name_plural = "Tables AO"  # Plural display name
    
class Marche(models.Model):
    site = models.CharField(max_length=100)
    numero_ao = models.CharField(max_length=100)
    designation = models.TextField()
    categorie = models.TextField(default='Default Category')
    ouverture_financiere = models.DateField()
    montant_dhht = models.DecimalField(max_digits=10, decimal_places=2)
    attributaire = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    def __str__(self):
        return self.numero_ao
    
    class Meta:
        verbose_name = "Marché attribue"  # Singular display name
        verbose_name_plural = "Marchés attribues"  # Plural display name
    
class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Abonné à")

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "Abonnement AO"  # Singular display name
        verbose_name_plural = "Abonnements AO"  # Plural display name



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    username = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)  # Updated to EmailField
    
    def __str__(self):
        return self.user.username
    
class DownloadHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Nom d'utilisateur")
    table_data = models.ForeignKey(TableData, on_delete=models.CASCADE , verbose_name="ID de document")
    download_timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Date de téléchargement")

    def __str__(self):
        return f"{self.user.username} downloaded {self.table_data.numero_ao} on {self.download_timestamp}"
    
    @classmethod
    def get_total_downloads(cls):
        return cls.objects.count()

    class Meta:
        verbose_name = "Historique de téléchargement"  # Singular display name
        verbose_name_plural = "Historiques de téléchargement"  # Plural display name
    
    
    
class UserRegistratione(models.Model):
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    activite = models.CharField(max_length=150, blank=True)
    categorie= models.CharField(max_length=150, blank=True, default='Default Category')
    adresse = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100, blank=True)
    telephone = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    password = models.CharField(max_length=128)  # Store plain password temporarily

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "Inscription des utilisateurs"  # Singular display name
        verbose_name_plural = "Inscriptions des utilisateurs"  # Plural display name
    




