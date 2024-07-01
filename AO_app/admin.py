from django.contrib import admin
from .models import TableData, Marche, ContactRequest, NewsletterSubscription , Profile,DownloadHistory,UserRegistratione
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render
from django.db.models import Count
from django.urls import path
import plotly.graph_objs as go
from plotly.offline import plot
from chartjs.views.lines import BaseLineChartView
from django.contrib.admin.models import LogEntry

admin.site.register(LogEntry)

# Override admin index template
admin.site.index_template = "admin/index.html"


class DownloadHistoryChart(BaseLineChartView):
    def get_labels(self):
        # Return a list of labels (x-axis)
        return ['January', 'February', 'March', 'April', 'May', 'June', 'July']

    def get_providers(self):
        # Return a list of dataset providers (legend entries)
        return ['Downloads']

    def get_data(self):
        # Return a list of datasets to plot
        data = [self.get_downloads_data()]
        return data

    def get_downloads_data(self):
        # Example: Return a list of download counts for each month
        # You can customize this based on your actual data structure
        # Example assumes you have a method to fetch monthly download counts
        # Adjust this as per your actual DownloadHistory model structure
        counts = [10, 20, 30, 40, 50, 60, 70]
        return counts


    



 
@admin.register(TableData)
class TableDataAdmin(admin.ModelAdmin):
    list_display = ('site', 'numero_ao','categorie', 'date_lancement')  # Specify fields to display in the list view
    search_fields = ('site', 'numero_ao','categorie', 'date_lancement')  # Add fields to search on in the admin


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_data', 'download_timestamp')
    search_fields = ['user__username', 'table_data__numero_ao']

    

    

    
    
@admin.register(UserRegistratione)
class UserRegistrationeAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'activite', 'ville')
    search_fields = ['username', 'activite']
    

    

@admin.register(Marche)
class MarcheAdmin(admin.ModelAdmin):
    list_display = ('site', 'numero_ao', 'designation', 'categorie')
    search_fields = ['site', 'numero_ao','categorie']

    

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('type_of_request', 'company_name', 'full_name', 'phone_number', 'email')
    search_fields = ['type_of_request', 'company_name','full_name']

    

    


admin.site.register(Profile)


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ['email', 'subscribed_at']
 


