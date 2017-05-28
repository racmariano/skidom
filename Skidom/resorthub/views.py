# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    return render(request, 'resorthub/index.html', {})

def userinfo(request):
    return HttpResponseRedirect(reverse('resorthub:index'))
