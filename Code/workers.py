from celery import Celery
from celery.schedules import crontab
from datetime import timedelta


celery_app = Celery("App Jobs")

# Create a subclass of task that wraps the task execution in an application context so its available

celery_app.config_from_object("configs.celeryConfig")

celery_app.conf.beat_schedule = {
    'userVisitNotif': {
        'task': 'tasks.sendVisitNotif',  # task path
        'schedule' : crontab(minute=00, hour=20)# Daily at 8 PM
    },
    'userMonthlyReport': {
        'task': 'tasks.sendMonthlyReports',  # task path
        'schedule' : crontab(minute=15, hour=15, day_of_month=1) # at 5:15 PM on the 1st of every month
    }
}