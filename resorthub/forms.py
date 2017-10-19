
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User
from users.models import UserProfile
from resorts.models import SkiPass, Resort

import datetime

class TripInformationForm(forms.Form):
    """ Gets user trip information on home page."""
    def __init__(self, *args, **kwargs):
        starting_from = kwargs.pop('starting_from')
        pass_id = kwargs.pop('pass_id')
        super(TripInformationForm, self).__init__(*args, **kwargs)
        self.fields['user_address'].initial = starting_from
        self.fields['pass_id'].initial = pass_id

    ski_passes = SkiPass.objects.all()

    user_address = forms.CharField(label = "Starting address", max_length = 200)
    search_date = forms.DateField(
        widget = forms.SelectDateWidget,
        label = "Date",
        initial = datetime.date.today
    )
    pass_id = forms.ModelChoiceField(
        label = "Look for resorts with what passes?",
        queryset = ski_passes,
    )

class CompareOrFavoriteForm(forms.Form):
    """ Gets relevant resorts from resort page """
    choices = forms.ModelMultipleChoiceField(
            queryset = Resort.objects.order_by('name'),
            widget = forms.CheckboxSelectMultiple, 
    )
