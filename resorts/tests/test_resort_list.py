from django.test import TestCase

from ..models import Resort, Conditions
from ..views import resort_list

USER_ADDRESS = '99 Brainerd Rd., Allston MA 02134'

class ResortListTestCase(TestCase):
    
    def setUp(self):
        Resort.objects.create(name="Hyrule", address="10 Rockefeller Plaza, New York, NY 10020")
        Resort.objects.create(name="Wachusset", address="499 Mountain Rd, Princeton, MA 01541")
        Resort.objects.create(name="Okemo", address="77 Okemo Ridge Rd, Ludlow, VT 05149")
        Resort.objects.create(name="Elvendale", address="1245 Worcester St, Natick Mall, Suite 2100, Natick, MA 01760")

    def test_on_distance(self):
        self.assertEquals(resort_list.get_resort_list(USER_ADDRESS, Resort.objects.all(),  order_on='distance'), [(u'Elvendale', {u'distance': 17.4, u'text_time': u'26 mins', u'time_in_seconds': 1576, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Wachusset', {u'distance': 56.5, u'text_time': u'1 hour 8 mins', u'time_in_seconds': 4095, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Okemo', {u'distance': 146.0, u'text_time': u'2 hours 54 mins', u'time_in_seconds': 10456, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Hyrule', {u'distance': 209.0, u'text_time': u'3 hours 36 mins', u'time_in_seconds': 12936, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'})])

    def test_on_snow(self):
        self.assertEquals(resort_list.get_resort_list(USER_ADDRESS, Resort.objects.filter(pk__lte=2), number_to_display = 15), [(u'Hyrule', {u'distance': 209.0, u'text_time': u'3 hours 36 mins', u'time_in_seconds': 12936, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Wachusset', {u'distance': 56.5, u'text_time': u'1 hour 8 mins', u'time_in_seconds': 4095, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'})]) 

    def test_on_time(self):
        self.assertEquals(resort_list.get_resort_list(USER_ADDRESS, Resort.objects.all(), number_to_display= 10, order_on='time_in_seconds'), [(u'Elvendale', {u'distance': 17.4, u'text_time': u'26 mins', u'time_in_seconds': 1576, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Wachusset', {u'distance': 56.5, u'text_time': u'1 hour 8 mins', u'time_in_seconds': 4095, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Okemo', {u'distance': 146.0, u'text_time': u'2 hours 54 mins', u'time_in_seconds': 10456, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'}), (u'Hyrule', {u'distance': 209.0, u'text_time': u'3 hours 36 mins', u'time_in_seconds': 12936, u'snow_in_past_24h': u'N/A', u'num_trails_open': u'N/A', u'base_temp': u'N/A'})]) 
