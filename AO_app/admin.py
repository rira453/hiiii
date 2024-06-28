from django.contrib import admin
from .models import TableData, Marche, ContactRequest, NewsletterSubscription , Profile,DownloadHistory,UserRegistratione
from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import login_required



@admin.register(TableData)
class TableDataAdmin(admin.ModelAdmin):
    list_display = ('site', 'numero_ao','categorie', 'date_lancement')  # Specify fields to display in the list view
    search_fields = ('site', 'numero_ao','categorie', 'date_lancement')  # Add fields to search on in the admin


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'table_data', 'download_timestamp')
    search_fields = ['user__username', 'table_data__numero_ao']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        # If search term is in `user__username` or `table_data__numero_ao`
        if search_term:
            queryset |= self.model.objects.filter(user__username__icontains=search_term) | \
                        self.model.objects.filter(table_data__numero_ao__icontains=search_term)
        
        return queryset, use_distinct
    
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



