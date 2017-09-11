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
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

from resorthub.models import Resort, UserProfile
from .forms import CustomUserCreationForm, EditProfileForm


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
            return redirect("/usersettings/profile", )

        else:
            messages.warning(request, 'There has been an error. Please try again!')
            return redirect("/usersettings/signup", )

    else:
        user_form = CustomUserCreationForm()
        return render(request, 'usersettings/signup.html', {'user_form': user_form })

@login_required()
def profile_view(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, user=request.user, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account was updated successfully.")
        return redirect("/usersettings/profile", )

    else:
        form = EditProfileForm(user=request.user)
        return render(request, 'usersettings/profile.html', {'form': form})
