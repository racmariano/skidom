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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

#Libraries for distance/time estimates
from django.contrib.gis.geoip2 import GeoIP2
import googlemaps
import json

#Import Objects
from .models import Resort, TrailPage
from .forms import UserAddressForm, CompareOrFavoriteForm

#Global variables
gmaps = googlemaps.Client(key='AIzaSyBRrCgnGFkdRY-Z1hX6xaxoUFBczNI2664')


#COMPARE AND RESORT LISTING METHOOOODSSS!!!
def resort_listing(request):
    if request.method == 'POST':
        selected_resort_ids = request.POST.getlist('choices[]')
        selected_resorts = Resort.objects.filter(pk__in=selected_resort_ids)
        if ("compare" in request.POST.keys()):
                if request.user.is_authenticated() and request.user.address != "":
                    starting_address = request.user.address
                else:
                    g = GeoIP2()
                    ip = request.META.get('REMOTE_ADDR', None)
                    if ip:
                        starting_address = g.city(ip)['city']
                    else:
                        starting_address = "Boston MA"

                return render(request, 'resorthub/compare.html', {'resorts': selected_resorts})
 
        elif ("favorite" in request.POST):
            if not request.user.is_authenticated():
                return redirect("/accounts/login/")
            else:
                request.user.favorite_resorts.add(*selected_resorts)
                request.user.save()
                messages.success(request, "Resorts added to favorites.")
                return redirect("/usersettings/profile/")
                
    else:
        resort_list = Resort.objects.order_by('name')
        return render(request, 'resorthub/resorts.html', {'resorts': resort_list})

def compare_listing(request, resort_list=Resort.objects.all()):
        return render(request, 'resorthub/compare.html', {'resorts': resort_list})


#RESORT HUB METHODS!!!!
def get_scraped_info(resort_list):
    trail_pages = [TrailPage.objects.get(resort=t.id) for t in resort_list]
    base_temps = [str(int(t.base_temp))+"° F" for t in trail_pages]
    num_open = [t.num_open for t in  trail_pages]
    new_snow =  [t.new_snow for t in trail_pages]

    return(base_temps, num_open, new_snow)

def index(request):
    resort_list = Resort.objects.all() 
    if request.method == 'POST':
        form = UserAddressForm(request.POST, pass_type = request.POST['pass_type'], starting_from = request.POST['user_address'])

        if form.is_valid():
            form_dict = process_form(request, form, resort_list)
            return render(request, 'resorthub/compare_options.html', form_dict)

        else:
            return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resort_list})


    else:
        header_message = "Where we\'d ski this weekend:"
        resort_list = Resort.objects.filter(pk__lte=10).exclude(url__exact='').order_by('name')

        if request.user.is_authenticated():
            address = request.user.address
            pass_type = request.user.pass_type            
            if len(request.user.favorite_resorts.all()) > 0:
                header_message = "What's up with your favorite resorts:"
                resort_list = request.user.favorite_resorts.all().order_by('name')

        else:
            address = 'Let\'s go!'
            pass_type = "NON"

        base_temps, num_open, new_snow = get_scraped_info(resort_list)

        form = UserAddressForm(pass_type = pass_type, starting_from=address) 
        return render(request, 'resorthub/index.html', {'form': form, 'header_message': header_message, 'supported_resorts': resort_list, 'base_temps': base_temps, 'trails_open': num_open, 'new_snow': new_snow})


def process_form(request, form, resort_list):
    address = form.cleaned_data['user_address']
    date = form.cleaned_data['search_date']
    pass_info = form.cleaned_data['pass_type'][0]
    sort_opt = form.cleaned_data['sort_opt']
    print(pass_info)

    #If we haven't made a crawler page, the url will be blank            
    filtered_resort_list = Resort.objects.filter(pk__lte=10, available_passes__contains=pass_info).exclude(url__exact='').order_by('name')
    print(filtered_resort_list.all())

    if not filtered_resort_list:
        return({'no_match': 1, 'form': form, 'supported_resorts': resort_list})

    resort_addresses = [x.address.raw for x in filtered_resort_list] 
    clean_dists, clean_times = use_googlemaps(address, resort_addresses)

    if not clean_dists:
        return({'invalid_address': 1, 'form': form, 'supported_resorts': resort_list})

    ordered_resort_info = order_resorts(sort_opt, filtered_resort_list, clean_dists, clean_times)
    ordered_resorts, ordered_dists, ordered_times, ordered_temps, ordered_open, ordered_snow = zip(*ordered_resort_info)

    return({'form': form, 'address': address, 'date': date, 'supported_resorts': ordered_resorts, 'distances': ordered_dists, 'times': ordered_times, 'base_temps': ordered_temps, 'trails_open':ordered_open, 'new_snow':ordered_snow,})



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
    base_temps, num_open, new_snow = get_scraped_info(filtered_resort_list)
    resort_info = zip(filtered_resort_list, clean_dists, clean_times, base_temps, num_open, new_snow)
    
    if sort_opt == "ABC":
        return(resort_info)    

    elif sort_opt == "TIM":
        return(time_order(resort_info))

    elif sort_opt == "DIS":
        i = 1
        flag = 0

    elif sort_opt == "WEA":
        i = 3
        flag = 1

    resort_info.sort(key = lambda t: t[i], reverse=flag)

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
