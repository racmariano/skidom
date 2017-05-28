# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .models import Resort
from .forms import UserAddressForm

def index(request): 
    resortlist = Resort.objects.order_by('resort_name')

    if request.method == 'POST':
        form = UserAddressForm(request.POST)

        if form.is_valid():
            address = form.cleaned_data['user_address']
            date = form.cleaned_data['search_date']
            maxx_only = form.cleaned_data['maxx_pass_only']
            
            if maxx_only:  
                resortlist = Resort.objects.filter(maxx_pass=True).order_by('resort_name')

            return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resortlist, 'input_flag': 1, 'address': address, 'date': date, 'maxx_only': maxx_only})

        else:
            return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resortlist})

    else:
        form = UserAddressForm() 
        return render(request, 'resorthub/index.html', {'form': form, 'supported_resorts': resortlist}) 
