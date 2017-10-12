# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# General imports
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages  

# Import Models
from .forms import TripInformationForm, CompareOrFavoriteForm
from resorts.models import Resort, SkiPass

# Import Views
from resorts.views import resorts_table

# Import GeoIP2 for location guessing
from django.contrib.gis.geoip2 import GeoIP2

def index(request):
    """ Home page for Skidom.

    On a GET request: Displays form for getting user trip details. 
    If user logged in and has favorite resorts, displays information
    about the five of them with the most 24h snow.
    Else, displays 5 resorts with the most 24h snow.

    On a POST request: Processes user trip detail form.
    Renders matching resorts and information to comparison template.

    Args:
        request (request): Page request.

    Returns:
        render: Renders valid resorts and info to comparison template
                if successful. Else, reloads the page.
    
    """
    resorts = Resort.objects.all() 

    if request.method == 'POST':
        form = TripInformationForm(request.POST, pass_id = request.POST['pass_id'], starting_from = request.POST['user_address'])

        if form.is_valid():
            if form.cleaned_data['user_address'] not in ["", "Let\'s go!"]:
                resorts = process_form(form)
                if resorts:
                    return render(request, 'resorthub/compare.html', {'resorts_list': resorts})
                else:
                    messages.warning(request, "No resorts matching criteria found. Please try again!")
                    return redirect('/')
                

            else:
                messages.warning(request, "Please enter a valid address!")
                return redirect('/')

    else:
        header_message = "Where we\'d ski this weekend:"

        if request.user.is_authenticated():
            address = request.user.address
            pass_id = request.user.pass_id            
            #if len(request.user.favorite_resorts.objects()) > 0:
            #    header_message = "What\'s up with your favorite resorts:"
            #    resorts = request.user.favorite_resorts.all()

        else:
            address = 'Let\'s go!'
            pass_id = None

        table = resorts_table(resorts, order_on = 'new_snow_24_hr')
        form = TripInformationForm(pass_id = pass_id, starting_from=address)
        return render(request, 'resorthub/index.html', {'form': form, 'header_message': header_message, 'resorts_list': table})


def process_form(form):
    """ Processes trip information form to get resort list for display.

    Args:
        form (Form): Posted trip information form 

    Returns:
        list: List of Resort dictionaries sorted by user choice and filtered by the pass option the user selected. 
              If no resorts with that pass are available, returns an empty list.

    """
    address = form.cleaned_data['user_address']
    pass_id = form.cleaned_data['pass_id']

    if pass_id:
        resorts = SkiPass.objects.get(name=pass_id).resorts.all()
    else:
        resorts = Resorts.objects.all()
    
    return(resorts_table(resorts, user_address = address, number_to_display = len(resorts)))


def resort_listing(request):
    """ Form page for either comparing selected resorts or adding them to the user's favorites.

    On a GET request, displays all available resorts and their relevant information. There are two
    buttons a user can use to make a POST request: either 'favorite' or 'compare.' As the information
    displayed is static, uses raw Resort objects. 

    On a POST request, if 'favorite' selected: if user not authenticated, the user is redirected to login page. If the 
    user is authenticated, selected resorts are added to user favorites, and the user is redirected
    to their profile. Elif 'compare' selected: selected resort information acquired, and information rendered
    to comparison template.

    Args:
        request (request): Page request

    Returns:
        Redirect or render based on criteria above. 

    """
    if request.method == 'POST':
        selected_resort_ids = request.POST.getlist('choices[]')
        selected_resorts = Resort.objects.filter(pk__in=selected_resort_ids)

        if ("compare" in request.POST.keys()):
                if request.user.is_authenticated() and request.user.address != None:
                    starting_address = request.user.address.formatted

                else:
        #We use GeoIP2 here to guess the starting address based on the user's IP.
                    g = GeoIP2()
                    ip = request.META['REMOTE_ADDR']
                    try:
                        starting_address = g.city(ip)['city'] 
                    except:        
                        starting_address = "Boston MA" 

                resorts_list = get_resort_list(selected_resorts, user_address = starting_address, number_to_display = len(selected_resorts), order_on='distance')

                return render(request, 'resorthub/compare.html', {'resorts_list': resorts_list})
 
        elif ("favorite" in request.POST.keys()):
            if not request.user.is_authenticated():
                return redirect("/accounts/login/")

            else:
                request.user.favorite_resorts.add(*selected_resorts)
                request.user.save()
                messages.success(request, "Resorts added to favorites.")
                return redirect("/usersettings/profile/")
                
    else:
        resorts_objects_list = Resort.objects.order_by('name')
        return render(request, 'resorthub/resorts.html', {'resorts_list': resorts_objects_list})


def compare_listing(request, resorts_list=[]):
    """ View for comparison page.

    Args:
        request (request): Page request
        resorts_list (list): List of Resort dictionaries

    Returns:
        render: Renders resorts_list to comparison template

    """
    return render(request, 'resorthub/compare.html', {'resorts_list': resorts_list})
