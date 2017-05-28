from django import forms

import datetime

class UserAddressForm(forms.Form):
    """
    Makes user data entry form for index. Gets location and date of trip.
    """
    user_address = forms.CharField(label = "Starting address", max_length = 200)
    search_date = forms.DateField(widget = forms.SelectDateWidget, label = "Date", initial = datetime.date.today)
