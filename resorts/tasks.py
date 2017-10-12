# Defining scraping tasks for Celery
from skidom.celery_setup import app

from celery import shared_task
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils

from models.resort import Resort

# See https://django-dynamic-scraper.readthedocs.io/en/latest/advanced_topics.html#scheduling-scrapers-checkers

@shared_task
def run_conditions_spiders():
    """ Celery task for updating Conditions objects """
    t = TaskUtils()

    # Optional, but can be used to refine scraping
    args = ()
    kwargs = {}

    t.run_spiders(Resort, 'scraper', 'scraper_runtime', 'conditions_spider')
