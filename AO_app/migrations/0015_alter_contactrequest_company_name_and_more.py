# Generated by Django 5.0.6 on 2024-08-02 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AO_app', '0014_alter_contactrequest_company_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Nom de l'entreprise"),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='full_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nom complet'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='industry',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="Secteur d'activité"),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Numéro de téléphone'),
        ),
        migrations.AlterField(
            model_name='contactrequest',
            name='type_of_request',
            field=models.CharField(choices=[("Demande d'info", "Demande d'info"), ('Reclamation', 'Reclamation'), ('Reclamation anonyme', 'Reclamation anonyme')], max_length=50, verbose_name='Type de demande'),
        ),
        migrations.AlterField(
            model_name='downloadhistory',
            name='download_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date de téléchargement'),
        ),
        migrations.AlterField(
            model_name='downloadhistory',
            name='table_data',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AO_app.tabledata', verbose_name='ID de document'),
        ),
        migrations.AlterField(
            model_name='downloadhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name="Nom d'utilisateur"),
        ),
        migrations.AlterField(
            model_name='newslettersubscription',
            name='subscribed_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Abonné à'),
        ),
    ]