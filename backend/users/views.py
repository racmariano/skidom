from __future__ import unicode_literals

# General imports
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic, View
from django.contrib import messages

# Libraries for user support
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm

# Relevant models and forms
from .models import UserProfile
from .forms import CustomUserCreationForm, EditProfileForm


def signup(request):
    """ Register account with Skidom.

    Args:
        request (request): Page request

    Returns:
        None. 
        If form is valid, new user added to database and redirected to profile page.

    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            new_user = UserProfile.objects.create_user(username, email=email, password=raw_password)            
            new_user.save()

            user = authenticate(username = username, password = raw_password)
            login(request, user)
            messages.success(request, "Awesome! Thank you so much for making an account!")
            return redirect("/users/profile", )

        else:
            messages.warning(request, 'There has been an error. Please try again!')
            return redirect("/users/signup", )

    else:
        user_form = CustomUserCreationForm()
        return render(request, 'users/signup.html', {'user_form': user_form })

@login_required()
def profile_view(request):
    """ View and update user profile.

    Args:
        request (request): Page request

    Returns:
        None. 
        If POST, relevant information added to UserProfile object and page refreshes.

    """
    if request.method == 'POST':
        form = EditProfileForm(request.POST, user=request.user, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, "Your account was updated successfully.")
        return redirect("/users/profile", )

    else:
        form = EditProfileForm(user=request.user)
        return render(request, 'users/profile.html', {'form': form})
