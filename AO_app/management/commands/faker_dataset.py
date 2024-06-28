from django.core.management.base import BaseCommand
from faker import Faker
import random
import pandas as pd
from django.contrib.auth.models import User

from AO_app.models import *

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for your models.'

    def handle(self, *args, **kwargs):
        num_records = 10

        # Generate data for each model
        contact_request_df = generate_contact_request_data(num_records)
        newsletter_subscription_df = generate_newsletter_subscription_data(num_records)
        profile_df = generate_profile_data(num_records)
        download_history_df = generate_download_history_data(num_records)
        user_registration_df = generate_user_registration_data(num_records)

        # Save data to database
        save_contact_request_data(contact_request_df)
        save_newsletter_subscription_data(newsletter_subscription_df)
        save_profile_data(profile_df)
        save_download_history_data(download_history_df)
        save_user_registration_data(user_registration_df)

        self.stdout.write(self.style.SUCCESS('Successfully generated and saved fake data.'))

categories = ['informatiques', 'assainissement', 'eau', 'electricité', 'transport', 'construction', 'travaux public']

def generate_moroccan_phone_number():
    return f"+212 6{random.randint(0, 5)} {''.join([str(random.randint(0, 9)) for _ in range(7)])}"

def generate_moroccan_address():
    return fake.street_address()

def generate_moroccan_city():
    moroccan_cities = ['Casablanca', 'Rabat', 'Marrakech', 'Fes', 'Agadir', 'Tanger', 'Meknes', 'Oujda', 'Kenitra', 'Beni Mellal', 'Asilah', 'Tetouan']
    return random.choice(moroccan_cities)

def generate_moroccan_fax_number():
    return f"+212 5{random.randint(0, 5)} {''.join([str(random.randint(0, 9)) for _ in range(7)])}"

def generate_contact_request_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            'type_of_request': random.choice(['Demande d\'info', 'Reclamation', 'Reclamation anonyme']),
            'company_name': fake.company(),
            'industry': fake.word(),
            'full_name': fake.name(),
            'phone_number': generate_moroccan_phone_number(),
            'email': fake.email(),
            'observations': fake.text()
        }
        data.append(record)
    return pd.DataFrame(data)

def generate_newsletter_subscription_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            'email': fake.email(),
            'subscribed_at': fake.date_time_this_year()
        }
        data.append(record)
    return pd.DataFrame(data)

def generate_profile_data(num_records):
    data = []
    for _ in range(num_records):
        user = User.objects.create(username=fake.user_name(), email=fake.email())
        record = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email
        }
        data.append(record)
    return pd.DataFrame(data)

def generate_download_history_data(num_records):
    data = []
    user_ids = list(User.objects.values_list('id', flat=True))
    table_data_ids = list(TableData.objects.values_list('id', flat=True))  # Fetch all TableData IDs
    for _ in range(num_records):
        record = {
            'user_id': random.choice(user_ids),
            'table_data_id': random.choice(table_data_ids),
            'download_timestamp': fake.date_time_this_year()
        }
        data.append(record)
    return pd.DataFrame(data)

def generate_user_registration_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            'username': fake.user_name(),
            'email': fake.email(),
            'activite': fake.word(),
            'categorie': random.choice(categories),
            'adresse': generate_moroccan_address(),
            'ville': generate_moroccan_city(),
            'telephone': generate_moroccan_phone_number(),
            'fax': generate_moroccan_fax_number(),
            'password': fake.password()
        }
        data.append(record)
    return pd.DataFrame(data)

def save_contact_request_data(df):
    for _, row in df.iterrows():
        ContactRequest.objects.create(
            type_of_request=row['type_of_request'],
            company_name=row['company_name'],
            industry=row['industry'],
            full_name=row['full_name'],
            phone_number=row['phone_number'],
            email=row['email'],
            observations=row['observations']
        )

def save_newsletter_subscription_data(df):
    for _, row in df.iterrows():
        NewsletterSubscription.objects.create(
            email=row['email'],
            subscribed_at=row['subscribed_at']
        )

def save_profile_data(df):
    for _, row in df.iterrows():
        Profile.objects.create(
            user_id=row['user_id'],
            username=row['username'],
            email=row['email']
        )

def save_download_history_data(df):
    for _, row in df.iterrows():
        DownloadHistory.objects.create(
            user_id=row['user_id'],
            table_data_id=row['table_data_id'],
            download_timestamp=row['download_timestamp']
        )

def save_user_registration_data(df):
    for _, row in df.iterrows():
        UserRegistratione.objects.create(
            username=row['username'],
            email=row['email'],
            activite=row['activite'],
            categorie=row['categorie'],
            adresse=row['adresse'],
            ville=row['ville'],
            telephone=row['telephone'],
            fax=row['fax'],
            password=row['password']
        )

# Define the number of records you want to generate
num_records = 10

# Generate data for each model
contact_request_df = generate_contact_request_data(num_records)
newsletter_subscription_df = generate_newsletter_subscription_data(num_records)
profile_df = generate_profile_data(num_records)
download_history_df = generate_download_history_data(num_records)
user_registration_df = generate_user_registration_data(num_records)

# Display the first few records of each DataFrame
print(contact_request_df.head())
print(newsletter_subscription_df.head())
print(profile_df.head())
print(download_history_df.head())
print(user_registration_df.head())
