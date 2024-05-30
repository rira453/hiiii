from django.contrib import admin
from .models import TableData, Marche, ContactRequest, NewsletterSubscription , Profile,DownloadHistory,UserRegistratione

admin.site.register(TableData)
admin.site.register(Marche)
admin.site.register(ContactRequest)
admin.site.register(DownloadHistory)
admin.site.register(Profile)
admin.site.register(UserRegistratione)
@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')

