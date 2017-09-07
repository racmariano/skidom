from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import UserProfile

import datetime

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields =  UserCreationForm.Meta.fields + ('email', 'address', 'favorite_runs', 'pass_type', 'own_equipment', 'favorite_resorts')


class UserAddressForm(forms.Form):
    """
    Makes user data entry form for index. Gets location and date of trip.
    """
 
    PASS_CHOICES = (("NON", "None"),
                    ("EPI", "Epic Pass"),
                    ("MAX", "Max Pass"),
                    ("MOC", "Mountain Collective Pass"),
                    ("NEP", "New England Pass"),
                    ("PEA", "Peak Pass"),
                    ("POW", "Powder Alliance Pass"),
                    ("ROC", "Rocky Mountain Super Pass"))

    SORT_OPTIONS = (("ABC", "Name"),
                    ("DIS", "Shortest distance"),
                    ("TIM", "Shortest time"),
                    ("SNO", "Most fresh snow"),
                    ("TRA", "Most trails open"))

    user_address = forms.CharField(label = "Starting address", max_length = 200)
    search_date = forms.DateField(widget = forms.SelectDateWidget, label = "Date", initial = datetime.date.today)
    pass_info = forms.MultipleChoiceField(label = "Look for resorts with what passes?", choices = PASS_CHOICES, required = True) 
    sort_opt = forms.ChoiceField(label="Sort results by:", choices = SORT_OPTIONS)

