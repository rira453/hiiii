# dashboards.py
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from admin_tools.dashboard import modules, Dashboard
from .models import DownloadHistory, Profile
from django.contrib.auth.models import User
from datetime import timedelta

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for your site.
    """

    def init_with_context(self, context):
        # Total downloads
        total_downloads = DownloadHistory.objects.count()

        # Downloads this week
        start_of_week = timezone.now() - timedelta(days=timezone.now().weekday())
        downloads_this_week = DownloadHistory.objects.filter(download_timestamp__gte=start_of_week).count()

        # Active users (assuming active users have logged in recently)
        active_users = User.objects.filter(last_login__gte=timezone.now() - timedelta(days=30)).count()

        # Add modules to the dashboard
        self.children.append(modules.LinkList(
            _('Summary'),
            children=[
                {
                    'title': _('Total Downloads'),
                    'url': '#',
                    'description': total_downloads,
                },
                {
                    'title': _('Downloads This Week'),
                    'url': '#',
                    'description': downloads_this_week,
                },
                {
                    'title': _('Active Users'),
                    'url': '#',
                    'description': active_users,
                },
            ]
        ))
