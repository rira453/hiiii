
from django_cron import CronJobBase, Schedule
from .views import deactivate_inactive_users

class DeactivateInactiveUsersCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # Run once a day

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'AO_app.deactivate_inactive_users_cron_job'  # a unique code

    def do(self):
        deactivate_inactive_users()
