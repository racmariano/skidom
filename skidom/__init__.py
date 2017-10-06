from __future__ import absolute_import, unicode_literals

# Make sure we always import celery when starting Django
from .celery import app as celery_app

