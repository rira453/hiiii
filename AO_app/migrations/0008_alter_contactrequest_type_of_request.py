# Generated by Django 5.0.6 on 2024-06-27 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AO_app', '0007_alter_contactrequest_type_of_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactrequest',
            name='type_of_request',
            field=models.CharField(choices=[("Demande d'info", "Demande d'info"), ('Reclamation', 'Reclamation'), ('Reclamation anonyme', 'Reclamation anonyme')], max_length=50),
        ),
    ]
