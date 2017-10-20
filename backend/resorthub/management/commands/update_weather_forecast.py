from django.core.management.base import BaseCommand, CommandError
from resorthub.models import Resort as Resort

import urllib2
import json

class Command(BaseCommand):
    help = 'Updates the snow forecast for the resort'

    def handle(self, *args, **options):
        resorts = Resort.objects.all()
        for resort in resorts:
            self.update_snow_forecast(resort)
        
    def update_snow_forecast(self, resort):
        locality = resort.address.locality.name
        state = resort.address.locality.state.name
        snow_forecast = self.get_snow_forecast(state, locality)
        num_to_string = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        for day, snowfall in enumerate(snow_forecast):
            setattr(resort, num_to_string[day] + '_day_snowfall', snowfall)
        resort.save()

    def get_snow_forecast(self, state, locality):
        f = urllib2.urlopen('http://api.wunderground.com/api/9c5a6634ac283749/forecast10day/q/' + state + '/' + locality + '.json')

        json_string = f.read()
        parsed_json = json.loads(json_string)
        forecast_days = parsed_json['forecast']['simpleforecast']['forecastday']
        snow_forecast = [day['snow_allday']['in'] for day in forecast_days]

        f.close()

        return snow_forecast

