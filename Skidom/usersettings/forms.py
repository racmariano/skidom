from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from resorthub.models import UserProfile, Resort

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields =  UserCreationForm.Meta.fields + ('email', 'address', 'favorite_runs', 'pass_type', 'own_equipment', 'favorite_resorts')


