# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

import googlemaps
import json

from .models import Resort
from .forms import UserAddressForm

gmaps = googlemaps.Client(key='AIzaSyBRrCgnGFkdRY-Z1hX6xaxoUFBczNI2664')

def index(request): 
    resort_list = Resort.objects.order_by('name')

    if request.method == 'POST':
        form = UserAddressForm(request.POST)

        if form.is_valid():
            form_dict = process_form(request, form, resort_list)
            return render(request, 'resorthub/index.html', form_dict)

        else:
            return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resort_list})

    else:
        form = UserAddressForm() 
        return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resort_list})


def process_form(request, form, resort_list):
    address = form.cleaned_data['user_address']
    date = form.cleaned_data['search_date']
    pass_info = form.cleaned_data['pass_info'][0]
            
    filtered_resort_list = Resort.objects.filter(available_passes__contains=pass_info).order_by('name')

    if not filtered_resort_list:
        return({'no_match': 1, 'form': form, 'supported_resorts': resort_list})

    resort_addresses = [x.address.raw for x in filtered_resort_list] 
    clean_dists, clean_times = use_googlemaps(address, resort_addresses)

    if not clean_dists:
        return({'invalid_address': 1, 'form': form, 'supported_resorts': resort_list})

    return({'form': form, 'address': address, 'date': date, 'supported_resorts': filtered_resort_list, 'distances': clean_dists, 'times': clean_times})


def use_googlemaps(address, resort_addresses):
    json_map_dists = gmaps.distance_matrix(origins = address, destinations = resort_addresses, mode = "driving", units = "imperial")

 
    clean_map_dists = []
    clean_map_times = [] 

    try: 
        for i in range(0, len(resort_addresses)):
            clean_map_dists.append(json_map_dists['rows'][0]['elements'][i]['distance']['text']) 
            clean_map_times.append(json_map_dists['rows'][0]['elements'][i]['duration']['text']) 
    
    except KeyError:
         return([], [])

    return(clean_map_dists, clean_map_times) 
