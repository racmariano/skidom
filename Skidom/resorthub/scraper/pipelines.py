import logging
from django.db.utils import IntegrityError
from django.forms import model_to_dict
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime

#Helper methods
def get_or_create(item, spider, crawled_url):
    model_class = getattr(item, 'django_model')
    exists = True

    try:
        obj = model_class.objects.get(url=crawled_url)
    except model_class.DoesNotExist:
        exists = False
        item['resort'] = spider.ref_object
        item['url'] = spider.scrape_url
        obj = item

    return (obj, exists)

def update_model(destination, source, spider, commit=True):
    try:
        pk = destination.pk
        fields_to_update = dict(source)
        for f in fields_to_update.keys():
            setattr(destination, f, source[f])
        
        print("Update successful")
        if commit:
            print("And saved")
            destination.save()
   
    except IntegrityError as e:
        spider.log(str(e), logging.ERROR)
        spider.log(str(item._errors), logging.ERROR)
        raise DropItem("Missing attribute.")

class UpdateOrCreatePipeline(object):
    def process_item(self, item, spider):
        if spider.conf['DO_ACTION']:
            commit = True
        else:
            commit = False

        if item.is_valid():    
            crawled_url = spider.start_urls[0]
            obj, trailpage_exists = get_or_create(item, spider, crawled_url)
            
            if not trailpage_exists:
                item = obj
                obj = item.instance            
    
            update_model(obj, item, commit)
                
        else:
            spider.log(str(item._errors), logging.ERROR)
            raise DropItem("Missing attribute.")

        return(item)

