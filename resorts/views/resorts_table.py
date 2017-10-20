# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# General imports
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

# Import Resort and Conditions models
from ..models import Resort, Conditions

# Imports for using Google Maps
import googlemaps
import json

import datetime

# Google Maps requires a client key to work
GMAPS = googlemaps.Client(key='AIzaSyBRrCgnGFkdRY-Z1hX6xaxoUFBczNI2664')

# Constants
NUMBER_TO_DISPLAY = 5
DEFAULT_ORDER_ON = 'new_snow_24_hr'

def resorts_table(selected_resorts, user_address = "", number_to_display = NUMBER_TO_DISPLAY, order_on = DEFAULT_ORDER_ON):
    """ Given a queryset of selected resorts, returns an ordered list of resort dictionaries and their conditions for display.
        
    If a user_address is supplied, also returns driving time and distance information.
    
    Args:
        selected_resorts (list): Queryset of Resorts
        user_address (str, optional): Indicates the user address
        number_to_display (int, optional): How many resorts we want to display
        order_on (str, optional): How we want to order the resort list. Should be key value for Resort dictionaries

    Returns:
        list: List of Resort dictionaries with name, id, condition information, and optional driving information

    """
    resorts_list = queryset_to_resort_dictionary(selected_resorts)

    if user_address != "":
        use_googlemaps(user_address, resorts_list)

    get_conditions(resorts_list) 

    return(order_resorts(resorts_list, number_to_display, order_on))

def queryset_to_resort_dictionary(selected_resorts):
    """ Gets needed ID, address, and website information from Resort models and returns
    list of Resort dictionaries.
    
    Args:
        selected_resorts (queryset): Queryset of Resorts        

    Returns:
        list: List of Resort dictionaries with name and id information

    """

    resorts_list = [x for x in selected_resorts.values('id', 'name', 'website')]

    for resort in resorts_list:
        resort_object = selected_resorts.get(pk=resort['id'])
        resort['our_take'] = resort_object.our_take

        try:
            resort['state'] = resort_object.address.locality.state.name
            resort['address'] = resort_object.address.formatted
        except:
            resort['address'] = resort_object.address.raw           

    return(resorts_list)

def use_googlemaps(address, resorts_list):
    """ We use the Google Maps API to get driving distances and times for the user.
    
    Google Maps returns a JSON response that we must parse.
    To see how the response object looks, visit: https://developers.google.com/maps/documentation/distance-matrix/intro.
    We keep the text-formatted times for display, as it's human-readable (A days B hours C minutes).
    We keep the time in seconds for easy sorting.

    Args:
        address (str): User address
        resorts_list (list): List of Resort dictionaries

    Returns:
        None.
        Resorts_list passed by reference. Relevant fields updated. 

    """ 
    for resort in resorts_list:
        json_map = GMAPS.distance_matrix(origins = address, destinations = resort['address'], mode = "driving", units = "imperial")

        try:
            # We grab the distance, chop off the trailing units using [:-3], and get rid of commas.
            # This allows us to process the distance as a float. 
            dist = float(json_map['rows'][0]['elements'][0]['distance']['text'][:-3].replace(',', ''))
            time_in_seconds = json_map['rows'][0]['elements'][0]['duration']['value']
            text_time = json_map['rows'][0]['elements'][0]['duration']['text']    
    
        except KeyError:
            dist = None
            time_in_seconds = None
            text_time = None

        resort['distance'] = dist 
        resort['time_in_seconds'] = time_in_seconds
        resort['text_time'] = text_time                                  

    
def get_conditions(resorts_list):
    """ Gets the associated Conditions report and adds this information to Resorts info. 

    If this information is not available (no Conditions object available), fill in with N/A.

    Args:
        resorts_list (list): List of Resort dictionaries

    Returns:
        None.
        Resorts_list passed by reference. Relevant fields updated.
    
    """
    for resort in resorts_list:
        try:
            resort_model = Resort.objects.get(name = resort["name"])
            t = Conditions.objects.filter(resort = resort_model)
            t = t.get(date = datetime.date.today())
            base_temp = str(int(t.base_temp))+"° F"
            num_trails_open = t.num_trails_open
            new_snow_24_hr = t.new_snow_24_hr            

        except ObjectDoesNotExist:
            base_temp = None
            num_trails_open = None
            new_snow_24_hr = None

        resort['base_temp'] = base_temp
        resort['num_trails_open'] = num_trails_open
        resort['new_snow_24_hr'] = new_snow_24_hr


def order_resorts(resorts_list, number_to_display, order_on):
    """ We want the highest base temperatures, amount of snow, and number of trails open.
    
    We want the lowest distances and times. The decreasing flag accounts for this.
    Sorts list based on order_on and returns a list with min(number_to_display, len(resorts_list)) elements

    Args:
        resorts_list (list): List of Resort dictionaries
        number_to_display (int, optional): How many resorts we want to display
        order_on (str, optional): How we want to order the resort list

    Returns:
        resorts_list (list): List of Resort dictionaries sorted using order_on 
                             with min(number_to_display, len(resorts_list)) elements 

    """    
    decreasing_flag = 1   

    if order_on in ['name', 'time_in_seconds', 'distance']:
            decreasing_flag = 0

    resorts_list.sort(key = lambda k: k[order_on], reverse = decreasing_flag)
 
    return(resorts_list[:min(number_to_display, len(resorts_list))]) 
