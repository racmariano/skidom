# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View

from .models import Resort
from .forms import UserAddressForm

class IndexView(generic.ListView):
    """
    Display currently supported resorts
    """
    model = Resort
    template_name = 'resorthub/index.html'
    context_object_name = 'supported_resorts'

    def get_queryset(self):
        return Resort.objects.order_by('resort_name')   


def userinfo(request):
    """
    Generate form object and update with user-supplied information 
    """
    input_flag = 0

    if request.method == 'POST':
        form = UserAddressForm(request.POST)

        if form.is_valid():
            input_flag = 1
            address = form.cleaned_data['user_address']
            date = form.cleaned_data['search_date']
            return render(request, 'index.html', {})

        else:
            return HttpResponseRedirect(reverse('resorthub:index'))

    else:

        form = UserAddressForm()  
        return render(request, 'index.html', {
           'form': form, 
        })
