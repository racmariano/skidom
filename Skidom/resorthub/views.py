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
    resortlist = Resort.objects.order_by('resort_name')

    if request.method == 'POST':
        form = UserAddressForm(request.POST)

        if form.is_valid():
            form_dict = process_form(request, form, resortlist)
            return render(request, 'resorthub/index.html', form_dict)

        else:
            return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resortlist})

    else:
        form = UserAddressForm() 
        return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resortlist})


def process_form(request, form, resortlist):
    address = form.cleaned_data['user_address']
    date = form.cleaned_data['search_date']
    maxx_only = form.cleaned_data['maxx_pass_only']
            
    if maxx_only:  
        resortlist = Resort.objects.filter(maxx_pass=True).order_by('resort_name')

    resort_addresses = [x.resort_address for x in resortlist] 

    clean_dists, clean_times = use_googlemaps(address, resort_addresses)

    if not clean_dists:
        return({'invalid_address': 1, 'form': form, 'supported_resorts': resortlist, 'maxx_only': maxx_only})

    return({'form': form, 'address': address, 'date': date, 'supported_resorts': resortlist, 'maxx_only': maxx_only,  'distances': clean_dists, 'times': clean_times})


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
