
from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *
from django.views.generic import RedirectView
admin.site.site_header = "La page d'administration du site des avis d'appels d'offres"
admin.site.site_title = "Dashboard"
admin.site.index_title = "Tableau de bord de l'administration"

urlpatterns = [
    
    path('admin/download_history_data/', views.download_history_data, name='download_history_data'),
     path('admin/contact_request_data/', views.contact_request_data, name='contact_request_data'),
      path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/', admin.site.urls),
    path('admin_tools_stats/',include('admin_tools_stats.urls')),
    
   
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('logout/', custom_logout_view, name='admin/logout/'),
    
    #path('jet/', include('jet.urls', 'jet')),
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('ao.html', views.ao, name='ao'),
    path('contact.html', views.contact_view, name='contact'),
    path('marches.html', views.marches, name='marches'),
    path('reglements.html', views.reglements, name='reglements'),
    path('demarches.html', views.demarches, name='demarches'),
    path('false.html', views.false, name='false'),
    path('investissement.html', views.investissement, name='investissement'),
    path('contact.html', views.contact_view, name='contact'),
    path('thank_you.html', views.contact_view, name='thank_you'),
    path('admine.html', views.admine, name='admine'),
    
    path('login.html', sing_in, name='sing_in'),
    path('register.html', sing_up, name='sing_up'),
    path('logout.html', log_out, name='log_out'),
    path('forgot_password.html', forgot_password, name='forgot_password'),
    path('update_password.html', update_password, name='update_password'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('update-password/<uidb64>/<token>/', update_password, name='update_password'),
    path('profile.html', profile_view, name='profile'),
    path('download_pdf/<int:pk>/', views.download_pdf, name='download_pdf'),
    path('admin/compose-email/', compose_email, name='compose_email'),
    path('charts.html/', views.download_history_chart, name='dashboard'),
     path('admin/newsletter_subscription_data/', views.newsletter_subscription_data, name='newsletter_subscription_data'),
    path('admin/download_history_data/', views.download_history_data, name='download_history_data'),
    path('admin/contact_request_data/', views.contact_request_data, name='contact_request_data'),
    
   
         ]
