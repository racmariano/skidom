from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from resorthub.models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields =  UserCreationForm.Meta.fields

    email = forms.EmailField(required=True)


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(EditProfileForm, self).__init__(*args, **kwargs)

        self.fields['address'].initial = user.address
        self.fields['email'].initial = user.email
        self.fields['favorite_runs'].initial = user.favorite_runs
        self.fields['favorite_resorts'].initial = user.favorite_resorts.all()
        self.fields['pass_type'].initial = user.pass_type
        self.fields['own_equipment'].initial = user.own_equipment


    class Meta:
        model = UserProfile
        fields = ('address', 'email', 'favorite_runs', 'favorite_resorts', 'pass_type', 'own_equipment')
