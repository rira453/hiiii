# AO_app/dashboard.py

from admin_tools.dashboard import Dashboard, modules

class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.children.append(modules.ModelList(title='Applications', models=('django.contrib.*',)))
        self.children.append(modules.RecentActions('Recent Actions', 5))
