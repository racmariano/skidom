# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#General imports
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

#Import Resort and ConditionsReport models
from ..models import Resort
from ...resorthub.models import TrailPage

#Imports for using Google Maps
import googlemaps
import json

#Google Maps requires a client key to work
GMAPS = googlemaps.Client(key='AIzaSyBRrCgnGFkdRY-Z1hX6xaxoUFBczNI2664')


def resort_list(user_address, selected_resorts, number_to_display=5, order_on='snow_in_past_24h'):
#Given a user address and selected resorts, return an ordered list of resorts for display
#We first use the Google Maps API to get distances and driving times for the journey between the user and the resorts
#We then use our scraped objects to get the 24 hr snow fall, temperatures at the mountain base, and number of trails open
#Finally, we return the sorted information as a list of tuples

    resorts_info = defaultdict()
    use_googlemaps(user_address, selected_resorts, resorts_info)
    get_conditions(selected_resorts, resorts_info) 
    return(order_resorts(resorts_info, number_to_display, order_on))


def use_googlemaps(address, selected_resorts, resorts_info):
#We use the Google Maps API to get driving distances and times for the user
#Google Maps returns a JSON response that we must parse
#For how to response object looks, see: https://developers.google.com/maps/documentation/distance-matrix/intro
#Grab the distance, chop off the trailing units using [:-3], and get rid of commas
#This allows us to process it as float 
#Keep the text-formatted times for output. It's human-readable (A days B hours C minutes)
#Keep the time in seconds for easy sorting without conversion

    for resort in selected_resorts:
        json_map = GMAPS.distance_matrix(origins = address, destinations = resort.address.raw, mode = "driving", units = "imperial")

        try:
            dist = float(json_map['rows'][0]['elements'][i]['distance']['text'][:-3].replace(',', ''))
            time_in_seconds = json_map['rows'][0]['elements'][i]['duration']['value']
            text_time = json_map['rows'][0]['elements'][i]['duration']['text']    
    
        except KeyError:
            dist = "N/A"
            time_in_seconds = "N/A"
            text_time = "N/A"

        resorts_info[resort.name]['distance'] = dist 
        resorts_info[resort.name]['time_in_seconds'] = time_in_seconds
        resorts_info[resort.name]['text_time'] = text_time                                  
    
def get_conditions(resort_list, resorts_info):
#Gets the associated Conditions report and adds this information to 
#Resorts info. If this information is not available (no Conditions object
#available), fill in with N/A

    for resort in resort_list:
        try:
            t = TrailPage.objects.get(resort=resort))
            base_temp = str(int(t.base_temp))+"° F")
            num_trails_open = t.num_open
            snow_in_past_24h = t.new_snow            

        except ObjectDoesNotExist:
            base_temp = "N/A"
            num_trails_open = "N/A"
            snow_in_past_24h = "N/A"

        resorts_info[resort.name]['base_temp'] = base_temp
        resorts_info[resort.name]['num_trails_open'] = num_trails_open
        resorts_info[resort.name]['snow_in_past_24h'] = snow_in_past_24h

def order_resorts(resorts_info, number_to_display, order_on):
#We want the highest base temperatures, amount of snow, and number of trails open
#We want the smallest distances and times
#The decreasing flag accounts for this
#Returns tuples of sorted resorts with (resort_name, resort_info for that resort)

    list_of_ordered_resorts = []
    decreasing_flag = 1

    if order_on == "alphabet":
        keys = sorted(resorts_info)        

    elif order_on is in ['time_in_seconds', 'distance']:
            decreasing_flag = 0

    keys = sorted(resorts_info, key = lambda x: resorts_info[x][order_on], reverse = decreasing_flag)

    for i in range(number_to_display-1):
        list_of_ordered_resorts.append((keys[i], resorts_info[keys[i]]))
    
    return(list_of_ordered_resorts) 
