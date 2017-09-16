from django.test import TestCase

from ..models import Resort
from ..views import resort_list

USER_ADDRESS = '99 Brainerd Rd., Allston MA 02134'

class ResortListTestCase(TestCase):
    
    def setUp(self):
        pass

    def sort_on_distance(self):
        print(resort_list(USER_ADDRESS, Resort.objects.all(),  order='distance'))

    def sort_on_snow(self):
        print(resort_list(USER_ADDRESS, Resort.objects.filter(pk__lte=10), number_to_display = 15))

    def sort_on_time(self):
        print(resort_list(USER_ADDRESS, Resort.objects.all(), number_to_display= 10, order='time_in_seconds')) 
