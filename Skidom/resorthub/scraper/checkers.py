from __future__ import unicode_literals
from dynamic_scraper.spiders.django_checker import DjangoChecker
from resorthub.models import TrailPage


class TrailPageChecker(DjangoChecker):

    name = 'trailpage_checker'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(TrailPage, **kwargs)
        self.scraper = self.ref_object.resort.scraper
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(ArticleChecker, self).__init__(self, *args, **kwargs)

