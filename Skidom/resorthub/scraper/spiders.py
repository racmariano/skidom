from dynamic_scraper.spiders.django_spider import DjangoSpider
from resorthub.models import Resort, TrailPage, TrailPageItem

class TrailSpider(DjangoSpider):

    name = 'trail_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(Resort, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = TrailPage
        self.scraped_obj_item_class = TrailPageItem
        super(TrailSpider, self).__init__(self, *args, **kwargs)


