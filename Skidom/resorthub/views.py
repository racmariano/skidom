# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
<<<<<<< HEAD

# Create your views here.
=======
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, skiing world")

>>>>>>> 86137960a9e8920087d8b0b16883e96d00eea37c
