# yourapp/management/commands/create_download_chart.py

from django.core.management.base import BaseCommand
from django.db.models import Count
import matplotlib.pyplot as plt
from AO_app.models import DownloadHistory  # Replace `yourapp` with your actual Django app name

class Command(BaseCommand):
    help = 'Create a chart showing download history'

    def handle(self, *args, **kwargs):
        # Query to get the number of downloads per user
        download_counts = DownloadHistory.objects.values('user__username').annotate(total_downloads=Count('id'))

        # Separate usernames and download counts for plotting
        usernames = [item['user__username'] for item in download_counts]
        download_counts = [item['total_downloads'] for item in download_counts]

        # Create a bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(usernames, download_counts, color='blue')
        plt.xlabel('Users')
        plt.ylabel('Number of Downloads')
        plt.title('Download History')

        # Rotate x-axis labels for better readability if there are many users
        plt.xticks(rotation=45, ha='right')

        # Show plot
        plt.tight_layout()
        plt.show()
