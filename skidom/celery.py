from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Setup Celery for automatic scraping
# See http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skidom.settings')

app = Celery('skidom')

# Configure
app.config_from_object('django.conf:settings')

# Load task modules
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
