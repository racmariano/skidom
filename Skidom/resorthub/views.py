# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#General imports
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
from .models import Resort
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
