# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# General imports
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages  
from django.core.exceptions import ObjectDoesNotExist

# Libraries for user support
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Import Objects
from .models import OldResort, TrailPage
from .forms import UserAddressForm, CompareOrFavoriteForm


def index(request):
    """ Home page for Skidom.

    On a GET request: Displays form for getting user trip details. 
    If user logged in and has favorite resorts, displays information
    about the five of them with the most 24h snow.
    Else, displays 5 resorts with the most 24h snow.

    On a POST request: Processes user trip detail form.
    Renders matching resorts and information to comparison template.

    Args:
        request: Page request.

    Returns:
        render: Renders valid resorts and info to comparison template
                if successful. Else, reloads the page.
    
    """
    resorts_list = OldResort.objects.all() 

    if request.method == 'POST':
        form = UserAddressForm(request.POST, pass_type = request.POST['pass_type'], starting_from = request.POST['user_address'])

        if form.is_valid():
            resorts_list = process_form(request, form)
            return render(request, 'resorthub/compare_options.html', resorts_list)

    else:
        header_message = "Where we\'d ski this weekend:"

        if request.user.is_authenticated():
            address = request.user.address
            pass_type = request.user.pass_type            
            if len(request.user.favorite_resorts.all()) > 0:
                header_message = "What\'s up with your favorite resorts:"
                resorts_list = request.user.favorite_resorts.all()

        else:
            address = 'Let\'s go!'
            pass_type = "NON"

        resorts_list = get_resort_list(resorts_list, filter_on="new_snow")
        form = UserAddressForm(pass_type = pass_type, starting_from=address)
 
        return render(request, 'resorthub/index.html', {'form': form, 'header_message': header_message, 'supported_resorts': resorts_list})


def process_form(request, form):
    """ Processes trip information form to get resort list for display.

    Args:
        request (request): Page request
        form (Form): Posted trip information form 

    Returns:
        list: List of Resort dictionaries sorted by user choice and filtered by the pass option the user selected. 
              If no resorts with that pass are available, returns an empty list.

    """
    address = form.cleaned_data['user_address']
    pass_info = form.cleaned_data['pass_type'][0]
    sort_opt = form.cleaned_data['sort_opt']

    filtered_resort_list = OldResort.objects.filter(available_passes__contains=pass_info)

    if not filtered_resort_list:
        return([])

    return(get_resort_list(filtered_resort_list, user_address = address, number_to_display = len(filtered_resort_list), order_on = sort_opt)


def resort_listing(request):
    if request.method == 'POST':
        selected_resort_ids = request.POST.getlist('choices[]')
        selected_resorts = OldResort.objects.filter(pk__in=selected_resort_ids)
        if ("compare" in request.POST.keys()):
                if request.user.is_authenticated() and request.user.address != "":
                    starting_address = request.user.address
                else:
                    starting_address = "Boston MA"

                resort_addresses = [x.address.raw for x in selected_resorts] 
                clean_dists, clean_times = use_googlemaps(starting_address, resort_addresses)

                return render(request, 'resorthub/compare.html', {
                    'resorts': selected_resorts,
                    'distances': clean_dists,
                    'times': clean_times,
                })
 
        elif ("favorite" in request.POST):
            if not request.user.is_authenticated():
                return redirect("/accounts/login/")
            else:
                request.user.favorite_resorts.add(*selected_resorts)
                request.user.save()
                messages.success(request, "Resorts added to favorites.")
                return redirect("/usersettings/profile/")
                
    else:
        resort_list = OldResort.objects.order_by('name')
        return render(request, 'resorthub/resorts.html', {'resorts': resort_list})

def compare_listing(request, resort_list=OldResort.objects.all()):
        return render(request, 'resorthub/compare.html', {'resorts': resort_list})


