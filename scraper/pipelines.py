# Imports for scraping
from django.db.utils import IntegrityError
from django.forms import model_to_dict
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime
import logging

# General imports
import datetime

# Helper methods
def get_or_create(item, spider):
    model_class = getattr(item, 'django_model')
    exists = True
    resort = spider.ref_object
    date = str(datetime.date.today())

    try:
        obj = model_class.objects.get(unique_id=resort.name+date)

    except model_class.DoesNotExist:
        print("Conditions report for %s on %s does not exist. Creating!" %(resort.name, date))
        exists = False
        item['resort'] = resort
        item['unique_id'] = resort.name+date
        item['conditions_page_url'] = spider.scrape_url
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
            obj, conditions_exists = get_or_create(item, spider)

            if not conditions_exists:
            # If doesn't exist, create toy instance and overwrite in update
                item = obj
                obj = item.instance

 
            update_model(obj, item, commit)
            spider.action_successful = True

        else:
            spider.log(str(item._errors), logging.ERROR)
            raise DropItem("Missing attribute.")

        return(item)
