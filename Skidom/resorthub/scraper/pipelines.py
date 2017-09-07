import logging
from django.db.utils import IntegrityError
from django.forms import model_to_dict
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime

#Helper methods
def get_or_create(item, crawled_url):
    model_class = getattr(item, 'django_model')
    exists = True

    try:
        obj = model_class.objects.get(url=crawled_url)
    except model_class.DoesNotExist:
        exists = False
        obj = item

    return (obj, exists)

def update_model(destination, source, commit=True):
    pk = destination.pk
    fields_to_update = dict(source)
    for f in fields_to_update.keys():
        setattr(destination, f, source[f])
    
    print("Update successful")
    if commit:
        print("And saved")
        destination.save()


def write_new_model(item, spider):
    try:
        item['resort'] = spider.ref_object

        checker_rt = SchedulerRuntime(runtime_type='C')
        checker_rt.save()
        item['checker_runtime'] = checker_rt

        item.save()
        spider.action_successful = True
        dds_id_str = str(item._dds_item_page) + '-' + str(item._dds_item_id)
        spider.struct_log("{cs}Item {id} saved to Django DB.{ce}".format(
            id=dds_id_str,
            cs=spider.bcolors['OK'],
            ce=spider.bcolors['ENDC']))
        print("New trail page created")
        
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
            obj, trailpage_exists = get_or_create(item, crawled_url)
            
            if trailpage_exists:
                update_model(obj, item, commit)
                
            elif commit:
                write_new_model(item, spider)            

        else:
            spider.log(str(item._errors), logging.ERROR)
            raise DropItem("Missing attribute.")

        return(item)

