from dynamic_scraper.spiders.django_spider import DjangoSpider
from resorts.models.resort import Resort
from resorts.models.conditions import Conditions, ConditionsItem

class ConditionsSpider(DjangoSpider):

    name = 'conditions_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(Resort, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.conditions_page_url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Conditions
        self.scraped_obj_item_class = ConditionsItem
        super(ConditionsSpider, self).__init__(self, *args, **kwargs)


