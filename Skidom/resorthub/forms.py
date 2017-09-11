from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from .models import UserProfile, Resort

import datetime

class UserAddressForm(forms.Form):
    """
    Makes user data entry form for index. Gets location and date of trip.
    """

    def __init__(self, *args, **kwargs):
        starting_from = kwargs.pop('starting_from')
        super(UserAddressForm, self).__init__(*args, **kwargs)
        self.fields['user_address'].initial = starting_from
 
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
                    ("TRA", "Most trails open"),
                    ("WEA", "Warmest base"),
                    )

    user_address = forms.CharField(label = "Starting address", max_length = 200)
    search_date = forms.DateField(widget = forms.SelectDateWidget, label = "Date", initial = datetime.date.today)
    pass_info = forms.MultipleChoiceField(label = "Look for resorts with what passes?", choices = PASS_CHOICES, required = True) 
    sort_opt = forms.ChoiceField(label="Sort results by:", choices = SORT_OPTIONS)



class CompareOrFavoriteForm(forms.Form):
    """ Gets relevant resorts from resort page """
    choices = forms.ModelMultipleChoiceField(
            queryset = Resort.objects.order_by('name'),
            widget = forms.CheckboxSelectMultiple, 
    )
