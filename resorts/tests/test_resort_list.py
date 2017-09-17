from django.test import TestCase

from ..models import Resort
from ..views import resort_list

TEST_USER_ADDRESS = '99 Brainerd Rd., Allston MA 02134'

class ResortListTestCase(TestCase):
    
    def setUp(self):
        Resort.objects.create(name="Hyrule", address="10 Rockefeller Plaza, New York, NY 10020")
        Resort.objects.create(name="Wachusett", address="499 Mountain Rd, Princeton, MA 01541")
        Resort.objects.create(name="Okemo", address="77 Okemo Ridge Rd, Ludlow, VT 05149")
        Resort.objects.create(name="Elvendale", address="1245 Worcester St, Natick Mall, Suite 2100, Natick, MA 01760")

    def test_order_on_distance(self):
        self.assertEquals(resort_list.get_resort_list(Resort.objects.all(), user_address=TEST_USER_ADDRESS, order_on='distance'), [{u'distance': 17.4, u'text_time': u'26 mins', u'name': u'Elvendale', u'time_in_seconds': 1576, u'id': 4, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 56.5, u'text_time': u'1 hour 8 mins', u'name': u'Wachusett', u'time_in_seconds': 4095, u'id': 2, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 146.0, u'text_time': u'2 hours 54 mins', u'name': u'Okemo', u'time_in_seconds': 10456, u'id': 3, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 209.0, u'text_time': u'3 hours 36 mins', u'name': u'Hyrule', u'time_in_seconds': 12936, u'id': 1, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}])

    def test_order_on_snow(self):
        self.assertEquals(resort_list.get_resort_list(Resort.objects.all(), number_to_display = 2), [{u'base_temp': u'N/A', u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'name': u'Hyrule', u'id': 5}, {u'base_temp': u'N/A', u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'name': u'Wachusett', u'id': 6}])

    def test_order_on_time(self):
        self.assertEquals(resort_list.get_resort_list(Resort.objects.all(), user_address=TEST_USER_ADDRESS, number_to_display= 10, order_on='time_in_seconds'), [{u'distance': 17.4, u'text_time': u'26 mins', u'name': u'Elvendale', u'time_in_seconds': 1576, u'id': 12, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 56.5, u'text_time': u'1 hour 8 mins', u'name': u'Wachusett', u'time_in_seconds': 4095, u'id': 10, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 146.0, u'text_time': u'2 hours 54 mins', u'name': u'Okemo', u'time_in_seconds': 10456, u'id': 11, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}, {u'distance': 209.0, u'text_time': u'3 hours 36 mins', u'name': u'Hyrule', u'time_in_seconds': 12936, u'id': 9, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}])
