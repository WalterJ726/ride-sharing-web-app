from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import RideDriver, RideOwner, RideSharer
from django.core.exceptions import ValidationError
from django.db import models

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password', 'email']

        
class DriverRegistrationForm(forms.ModelForm):
    class Meta:
        model = RideDriver
        fields = ['vehicle_type', 'plate_num', 'max_passengers', 'special_request']


class RideRequestForm(forms.ModelForm):
    #arrival = forms.DateTimeField(widget=forms.SplitDateTimeWidget(date_attrs={"type": "date"}, time_attrs={"type": "time"}))
    
    class Meta:
        model = RideOwner
        fields = ['dest_addr', 'arrival', 'num_passenger', 'vehicle_type', 'special_request', 'sharable']
        labels = {
            'dest_addr': 'Destination',
            'arrival': 'Arrival Time',
        }


class RideSearchForm(forms.ModelForm):
    class Meta:
        model = RideSharer
        fields = ['dest_addr', 'arrival_start', 'arrival_end', 'num_passengers']
        labels = {
            'dest_addr': 'Destination',
        }

    def clean(self):
        start = self.cleaned_data.get('arrival_start')
        end = self.cleaned_data.get('arrival_end')
        if start and end and start >= end:
            raise ValidationError("Invalid arrival time window! 'Arrival start' should be less than 'Arrival end'")
        return self.cleaned_data
