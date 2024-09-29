from celery import Celery
import os

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'turbo_az.settings')

# Create the Celery app instance
app = Celery('turbo_az')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in installed apps.
app.autodiscover_tasks()
