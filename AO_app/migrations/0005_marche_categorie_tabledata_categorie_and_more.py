# Generated by Django 5.0.6 on 2024-06-26 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AO_app', '0004_userregistratione_downloadhistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='marche',
            name='categorie',
            field=models.TextField(default='Default Category'),
        ),
        migrations.AddField(
            model_name='tabledata',
            name='categorie',
            field=models.TextField(default='Default Category'),
        ),
        migrations.AddField(
            model_name='userregistratione',
            name='categorie',
            field=models.CharField(blank=True, default='Default Category', max_length=150),
        ),
    ]
