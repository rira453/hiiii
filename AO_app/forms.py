from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import NewsletterSubscription
from .models import ContactRequest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['type_of_request', 'company_name', 'industry', 'full_name', 'phone_number', 'email', 'observations']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Expression régulière pour les numéros de téléphone marocains
        if not re.match(r'^0[5-7]\d{8}$', phone_number):
            raise ValidationError("Veuillez entrer un numéro de téléphone marocain valide.")
        return phone_number

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0 rounded-pill w-100 ps-4 pe-5',
                'placeholder': 'Saisir votre email',
                'style': 'height: 48px;',
            })
        }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    activite = forms.CharField(max_length=100, required=True)
    adresse = forms.CharField(max_length=255, required=True)
    ville = forms.CharField(max_length=100, required=True)
    telephone = forms.CharField(max_length=20, required=True)
    fax = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address already exists!")
        return email
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['username', 'email'] 