from django.test import TestCase

# Import relevant models
from resorthub.models import OldResort
from address.models import AddressField

# Import the function we want to test
from ..views import resort_list



TEST_USER_ADDRESS = '99 Brainerd Rd., Allston MA 02134'

class ResortListTestCase(TestCase):
    
    def setUp(self):
        OldResort.objects.create(name="Hyrule", address="10 Rockefeller Plaza, New York, NY 10020")
        OldResort.objects.create(name="Wachusett", address= "499 Mountain Rd, Princeton, MA 01541")
        OldResort.objects.create(name="Okemo", address= "77 Okemo Ridge Rd, Ludlow, VT 05149")
        OldResort.objects.create(name="Elvendale", address= "1245 Worcester St, Natick Mall, Suite 2100, Natick, MA 01760")

    def test_order_on_distance(self):
        resorts_list = resort_list.get_resort_list(OldResort.objects.all(), user_address=TEST_USER_ADDRESS, order_on='distance')
        resorts_names = [x['name'] for x in resorts_list]
        self.assertEquals(resorts_names, ['Elvendale', 'Wachusett', 'Okemo', 'Hyrule'])

    def test_order_on_snow(self):
        resorts_list = resort_list.get_resort_list(OldResort.objects.all(), number_to_display = 2)
        resorts_names = [x['name'] for x in resorts_list]
        self.assertEquals(resorts_names, ['Hyrule', 'Wachusett'])

    def test_order_on_time(self):
        resorts_list = resort_list.get_resort_list(OldResort.objects.all(), user_address=TEST_USER_ADDRESS, number_to_display= 10, order_on='time_in_seconds')
        resorts_names = [x['name'] for x in resorts_list]
        self.assertEquals(resorts_names, ['Elvendale', 'Wachusett', 'Okemo', 'Hyrule'])

