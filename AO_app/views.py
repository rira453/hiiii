
from django.shortcuts import render,HttpResponse, redirect,  get_object_or_404
from .forms import ContactForm, NewsletterForm
from .models import ContactRequest, TableData, Marche 
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.core.validators import validate_email
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
from AO_app import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.http import FileResponse, Http404
from .models import *
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django import forms
import plotly.express as px





def ao(request):
    data = TableData.objects.all()
    return render(request, 'ao.html', {'data': data})

def reglements(request):
    return render(request, 'reglements.html')

def false(request):
    return render(request, 'false.html')

def marches(request):
    marches = Marche.objects.all()
    return render(request, 'marches.html', {'marches': marches})

def demarches(request):
    return render(request, 'demarches.html')

def investissement(request):
    return render(request, 'investissement.html')

def doc(request):
    return render(request, 'doc.html')

def admine(request):
    return render(request, 'admin/admine.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Merci pour votre message!")
            return redirect('contact')
        else:
            messages.error(request, "Il y a eu une erreur dans votre soumission.")
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def index(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for subscribing!")
            return redirect('index')
        else:
            messages.error(request, "There was an error with your subscription.")
    else:
        form = NewsletterForm()
    return render(request, 'index.html', {'form': form})




# Create your views here.
from django.views.decorators.cache import never_cache

@never_cache  # Apply never_cache decorator to prevent caching of the login page
def sing_in(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect authenticated users to the home page or any other page

    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('index')  # Redirect to home page after login
            else:
                messages.error(request, "Mot de passe incorrect")
        else:
            # Check if user exists in UserRegistration table
            user_reg = UserRegistratione.objects.filter(email=email, password=password).first()
            if user_reg:
                # Transfer data to auth_user table
                user = User.objects.create_user(
                    username=user_reg.username,
                    email=user_reg.email,
                    password=user_reg.password,
                )
                user.save()
                # Authenticate and log in the user
                auth_user = authenticate(username=user.username, password=user_reg.password)
                if auth_user:
                    login(request, auth_user)
                    return redirect('index')
            else:
                messages.error(request, "Utilisateur non trouvé")

    return render(request, 'login.html', {})  # Display login form (login.html)

from .models import UserRegistratione
from django.contrib.auth.hashers import make_password


def sing_up(request):
    error = False
    message = ""

    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        activite = request.POST.get('activite', None)
        categorie = request.POST.get('categorie', None)
        adresse = request.POST.get('adresse', None)
        ville = request.POST.get('ville', None)
        telephone = request.POST.get('telephone', None)
        fax = request.POST.get('fax', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)

        # Validation de l'email
        try:
            validate_email(email)
        except:
            error = True
            message = "Entrez un email valide s'il vous plaît !"

        # Validation des mots de passe
        if not error:
            if password != repassword:
                error = True
                message = "Les deux mots de passe ne correspondent pas !"

        # Vérification de l'existence de l'utilisateur
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec l'email {email} ou le nom d'utilisateur {name} existe déjà !"
        if len(name) > 20:
            error = True
            message = "Le nom d'utilisateur doit contenir moins de 20 caractères !"
        if not name.isalnum():
            error = True
            message = "Le nom d'utilisateur doit être alphanumérique !"

        # Enregistrement de l'utilisateur
        if not error:
            # Save registration information in UserRegistratione table with hashed password
            user_reg = UserRegistratione(
                username=name,
                email=email,
                activite=activite,
                categorie=categorie,
                adresse=adresse,
                ville=ville,
                telephone=telephone,
                fax=fax,
                password=make_password(password)  # Hash the password
            )
            user_reg.save()

            # Create and save the User object
            user = User(
                username=name,
                email=email,
            )
            user.set_password(password)  # Set the password for the user
            user.is_active = False  # Set user as inactive until email confirmation
            user.save()

            messages.success(request, "Votre compte a été créé! Veuillez vérifier votre courrier électronique pour confirmer votre adresse e-mail afin d'activer votre compte.")

            subject = "Bienvenue sur notre site web!"
            message = f"Bonjour {activite}!! \nBienvenue!! \nMerci de visiter notre site web. Nous vous avons envoyé un e-mail de confirmation, veuillez confirmer votre adresse e-mail. \n\nMerci Beaucoup\nVeolia"
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirmez votre adresse e-mail"
            message2 = render_to_string('Email.html', {
                'name': name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            
            email = EmailMessage(
                email_subject,
                message2,
                from_email,
                [email],
            )
            email.content_subtype = 'html'  # Specify HTML content
            email.send(fail_silently=True)
            return redirect('sing_in')  # Redirection vers la page de connexion après l'inscription

    context = {
        'error': error,
        'message': message
    }

    return render(request, 'register.html', context)
@login_required(login_url='sing_in')
def dashboard(request):
    return render(request, 'admin.html', {})
from django.http import HttpResponseRedirect
@never_cache
def log_out(request):
    logout(request)
    response = HttpResponseRedirect('index.html')  # Redirect to the login page
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
    response['Pragma'] = 'no-cache'  # HTTP 1.0.
    response['Expires'] = '0'  # Proxies.
    return response


def forgot_password(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            print("processing forgot password")
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('update_password', kwargs={'uidb64': uid, 'token': token})
            )

            html = render_to_string('password_reset_email.html', {'reset_url': reset_url})

            msg = EmailMessage(
                "Modification de mot de passe!",
                html,
                "ayaboulifa8@gmail.com",
                [email],
            )

            msg.content_subtype = 'html'
            msg.send()
            
            message = "Un email a été envoyé avec les instructions pour réinitialiser votre mot de passe."
            success = True
        else:
            print("L'utilisateur n'existe pas")
            error = True
            message = "L'utilisateur n'existe pas"
    
    context = {
        'success': success,
        'error': error,
        'message': message
    }
    return render(request, "forgot_password.html", context)
def update_password(request, uidb64=None, token=None):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and confirm_password and new_password == confirm_password:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, "Votre mot de passe a été mis à jour avec succès.")
                    return redirect('sing_in')  # Assurez-vous que 'login' correspond à votre nom de route de connexion
                else:
                    messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
            except User.DoesNotExist:
                messages.error(request, "L'utilisateur n'existe pas.")
        else:
            messages.error(request, "Les mots de passe ne correspondent pas.")

    context = {
        'uidb64': uidb64,
        'token': token
    }
    return render(request, "update_password.html", context)


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Votre Compte est activée!!")
        return redirect('sing_in')
    else:
        return render(request,'activation_failed.html')

from .models import Profile
from .forms import ProfileForm

@login_required
@never_cache
def profile_view(request):
    
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user, username=user.username, email=user.email)
    
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    
    return render(request, 'profile.html', {'form': form})

@login_required
def download_pdf(request, pk):
    try:
        table_data = TableData.objects.get(pk=pk)
        if table_data.pdf_file:
            # Log the download
            DownloadHistory.objects.create(user=request.user, table_data=table_data)
            return FileResponse(table_data.pdf_file.open(), as_attachment=True, filename=table_data.pdf_file.name)
        else:
            raise Http404
    except TableData.DoesNotExist:
        raise Http404

    


from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def view_download_history(request):
    download_history = DownloadHistory.objects.all()

    return render(request, 'admin/view_download_history.html', {'download_history': download_history})


from plotly.offline import plot
import plotly.graph_objs as go
def download_history_chart(request):
    # Query data for the chart
    download_history = DownloadHistory.objects.all()

    # Prepare data for the chart
    timestamps = [history.download_timestamp for history in download_history]
    user_names = [history.user.username for history in download_history]

    # Create a Plotly figure
    fig = go.Figure([go.Bar(x=timestamps, y=user_names)])
    fig.add_trace(go.Scatter(x=timestamps, y=user_names, mode='markers', name='Downloads'))

    # Customize layout
    fig.update_layout(title='Download History',
                      xaxis_title='Timestamp',
                      yaxis_title='User',
                      template='plotly_dark')  # Optional: Choose a Plotly theme

    # Convert the figure to JSON and render it in the template
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    context = {'plot_div': plot_div}
    return render(request, 'charts.html', context)

def download_history_admin(request):
    download_history = DownloadHistory.objects.all()

    # Prepare data for the chart
    timestamps = [history.download_timestamp for history in download_history]
    user_names = [history.user.username for history in download_history]

    # Create a Plotly figure
    fig = go.Figure([go.Bar(x=timestamps, y=user_names)])
    fig.add_trace(go.Scatter(x=timestamps, y=user_names, mode='markers', name='Downloads'))

    # Customize layout
    fig.update_layout(title='Download History',
                      xaxis_title='Timestamp',
                      yaxis_title='User',
                      template='plotly_dark')  # Optional: Choose a Plotly theme

    # Convert the figure to JSON and render it in the template
    plot_div = plot(fig, output_type='div', include_plotlyjs=False)

    context = {'plot_div': plot_div}
    return render(request, 'admin/index.html', context)

#######################################""
def download_history_data(request):
    # Example: Count downloads per day
    downloads = DownloadHistory.objects.extra(select={'day': 'date( download_timestamp )'}).values('day').annotate(count=Count('id')).order_by('day')
    
    data = {
        "labels": [download['day'] for download in downloads],
        "data": [download['count'] for download in downloads],
    }
    return JsonResponse(data)

def contact_request_data(request):
    requests = ContactRequest.objects.values('type_of_request').annotate(count=Count('id')).order_by('type_of_request')
    
    data = {
        "labels": [request['type_of_request'] for request in requests],
        "data": [request['count'] for request in requests],
    }
    return JsonResponse(data)

from datetime import datetime, timedelta

def admin_dashboard(request):
    # Total number of downloads
    total_downloads = DownloadHistory.objects.count()
    
    # Total number of users
    total_users = User.objects.count()
    
    # Total number of new users this week
    start_of_week = timezone.now() - timezone.timedelta(days=timezone.now().weekday())
    new_users_this_week = User.objects.filter(date_joined__gte=start_of_week).count()

    print(f"Total Downloads: {total_downloads}")
    print(f"Total Users: {total_users}")
    print(f"New Users This Week: {new_users_this_week}")

    context = {
        'total_downloads': total_downloads,
        'total_users': total_users,
        'new_users_this_week': new_users_this_week,
    }
    return render(request, 'admin/index.html', context)



#############################################""
def admin_dashboard(request):
    total_downloads = DownloadHistory.objects.count()
    print(f"Total downloads: {total_downloads}") 

    context = {
        'total_downloads': total_downloads,
        # Add other context variables as needed
    }

    return render(request, 'admin/index.html', context)

from django.utils import timezone
from datetime import timedelta

from django.conf import settings

def deactivate_inactive_users():
    three_months_ago = timezone.now() - timedelta(days=90)
    inactive_users = User.objects.filter(last_login__lt=three_months_ago, is_active=True)
    for user in inactive_users:
        user.is_active = False
        user.save()
        
        # Send email notification
        subject = "Account Deactivation Notice"
        message = f"Dear {user.username},\n\nYour account has been deactivated due to inactivity for over three months. Please contact support to reactivate your account.\n\nBest regards,\nAmendis"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [user.email]
        
        send_mail(subject, message, from_email, to_email)
        
    print(f"Deactivated {inactive_users.count()} users and sent emails")

def index(request):
    table_data = TableData.objects.all()  # Query all instances of TableData
    total_downloads = 100  # Example, replace with your actual logic to calculate total downloads

    context = {
        'table_data': table_data,
        'total_downloads': total_downloads,
    }

    return render(request, 'admin/index.html', context)
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Count
from .models import DownloadHistory

def download_history_chart(request):
    # Query the DownloadHistory model to get the data
    download_history = DownloadHistory.objects.all()

    # Prepare data for the chart
    chart_data = [['User', 'Number of Downloads']]
    for history in download_history:
        chart_data.append([history.user.username, history.user.downloadhistory_set.count()])

    context = {
        'chart_data': chart_data,
    }
    return render(request, 'admin/index.html', context)

from django.shortcuts import redirect

def custom_logout_view(request):
    logout(request)
    return redirect('/admin/login/')

from django.shortcuts import render
from django.utils import timezone
from .models import UserRegistratione, DownloadHistory, TableData
from datetime import timedelta
from django.db import models 

def dashboard(request):
    # Calculate the number of new members
    one_month_ago = timezone.now() - timedelta(days=30)
    new_members = UserRegistratione.objects.filter(date_joined__gte=one_month_ago).count()
    
    # Get download history
    download_history = DownloadHistory.objects.all()
    
    # Count downloads per document
    document_downloads = (
        DownloadHistory.objects
        .values('table_data__designation')
        .annotate(download_count=models.Count('id'))
    )

    context = {
        'new_members': new_members,
        'download_history': download_history,
        'document_downloads': document_downloads,
    }

    return render(request, 'dashboard.html', context)


class EmailForm(forms.Form):
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)
    subject = forms.CharField(max_length=255)
    message = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)

def compose_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            recipients = form.cleaned_data['recipients']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            attachment = request.FILES.get('attachment')

            email = EmailMessage(subject, message, to=[user.email for user in recipients])
            if attachment:
                email.attach(attachment.name, attachment.read(), attachment.content_type)
            email.send()

            return redirect('admin:index')
    else:
        form = EmailForm()

    return render(request, 'admin/compose_email.html', {'form': form})