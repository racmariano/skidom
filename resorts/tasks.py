# Defining scraping tasks for Celery
from __future__ import absolute_import, unicode_literals
from celery import shared_task

from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils

from .models.resort import Resort

# See https://django-dynamic-scraper.readthedocs.io/en/latest/advanced_topics.html#scheduling-scrapers-checkers

@shared_task
def run_spiders():
    """ Celery task for updating Conditions objects """
    t = TaskUtils()

    t.run_spiders(Resort, 'scraper', 'scraper_runtime', 'conditions_spider')
