# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#General imports
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages  

#Libraries for user support
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

#Libraries for distancce/time estimates
import googlemaps
import json

#Import Objects
from .models import Resort, TrailPage
from .forms import UserAddressForm, CustomUserCreationForm

#Global variables
gmaps = googlemaps.Client(key='AIzaSyBRrCgnGFkdRY-Z1hX6xaxoUFBczNI2664')



#USER CREATION METHODS!!!
#This code was copied and then modified from the website simpleisbetterthancomplex

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            messages.success(request, "Awesome! Thank you so much for making an account!")
            return redirect("/resorthub/", )

        else:
            messages.warning(request, 'There has been an error. Please try again!')
            return redirect("/resorthub/signup", ) 

    else:
        user_form = CustomUserCreationForm()
        return render(request, 'resorthub/signup.html', {'user_form': user_form })

def resort_listing(request):
    resort_list = Resort.objects.order_by('name')
    return render(request, 'resorthub/resorts.html', {'resorts': resort_list})


#RESORT HUB METHODS!!!!
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
    sort_opt = form.cleaned_data['sort_opt']
            
    filtered_resort_list = Resort.objects.filter(available_passes__contains=pass_info).order_by('name')

    if not filtered_resort_list:
        return({'no_match': 1, 'form': form, 'supported_resorts': resort_list})

    resort_addresses = [x.address.raw for x in filtered_resort_list] 
    clean_dists, clean_times = use_googlemaps(address, resort_addresses)

    if not clean_dists:
        return({'invalid_address': 1, 'form': form, 'supported_resorts': resort_list})

    ordered_resort_info = order_resorts(sort_opt, filtered_resort_list, clean_dists, clean_times)
    ordered_resorts, ordered_dists, ordered_times, ordered_temps = zip(*ordered_resort_info)

    return({'form': form, 'address': address, 'date': date, 'supported_resorts': ordered_resorts, 'distances': ordered_dists, 'times': ordered_times, 'temps': ordered_temps})



def use_googlemaps(address, resort_addresses):
    json_map_dists = gmaps.distance_matrix(origins = address, destinations = resort_addresses, mode = "driving", units = "imperial")

 
    clean_map_dists = []
    clean_map_times = [] 

    try: 
        for i in range(0, len(resort_addresses)):
            
            dist = json_map_dists['rows'][0]['elements'][i]['distance']['text'][:-3].replace(',', '')
            clean_map_dists.append(float(dist)) 
            clean_map_times.append(json_map_dists['rows'][0]['elements'][i]['duration']['text']) 
    
    except KeyError:
         return([], [])

    return(clean_map_dists, clean_map_times)

def order_resorts(sort_opt, filtered_resort_list, clean_dists, clean_times):
    temps = [TrailPage.objects.get(resort=t.id).base_temp for t in filtered_resort_list]

    resort_info = zip(filtered_resort_list, clean_dists, clean_times, temps)
    
    if sort_opt == "ABC":
        return(resort_info)    

    elif sort_opt == "TIM":
        return(time_order(resort_info))

    elif sort_opt == "DIS":
        i = 1

    elif sort_opt == "WEA":
        i = 3

    resort_info.sort(key = lambda t: t[i], reverse=True)

    return(resort_info) 

def time_order(resort_info):
#Takes in zipped list of [(resorts, distances, times)] and converts string times to sum of minutes.
#Returns sorted list based on sums of minutes.

    minute_times = []

    for resort in resort_info:
        time_in_minutes = 0
        google_time = resort[2]
    
        if 'day' in google_time:
            parsed_time = re.split('day[s]? ', google_time)
            time_in_minutes += 1440*int(parsed_time[0])
            google_time = parsed_time[1]

        if 'hour' in google_time:
            parsed_time = re.split('hour[s]? ', google_time)
            time_in_minutes += 60*int(parsed_time[0]) 
            google_time = parsed_time[1]    

        if 'min' in google_time:
            parsed_time = re.split('min[s]?', google_time)
            time_in_minutes += int(parsed_time[0]) 

        minute_times.append(time_in_minutes)

    resorts_with_times = zip(resort_info, minute_times)
    resorts_with_times.sort(key = lambda t: t[1])
    sorted_resorts = zip(*resorts_with_times)[:-1]
    return(sorted_resorts[0])
