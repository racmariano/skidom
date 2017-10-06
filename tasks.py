# Defining scraping tasks for Celery

from celery.task import task
from django.db.models import Q
from dynamic_scraper.utils.task_utils import TaskUtils

# Using old reshorthub TrailPage models, as these are properly implemented
# Will switch when migration is complete
from resorthub.models import TrailPage

# See https://django-dynamic-scraper.readthedocs.io/en/latest/advanced_topics.html#scheduling-scrapers-checkers

@task()
def run_conditions_spiders():
    """ Celery task for updating Conditions objects """
    t = TaskUtils()

    t.run_conditions_spiders(TrailPage, 'scraper', 'scraper_runtime', 'trail_spider', *args, **kwargs)
