from django import forms
from . import models
from catalog.utils.bootstrap import BootStrapForm, BootStrapModelForm
from catalog.utils.encrypt import md5
from django.core.exceptions import ValidationError

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="username",
        widget=forms.TextInput(),
        required=True,
    )

    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput(render_value=True),
        required=True,
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

class RegisterModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.User
        fields = ['username', 'password', 'confirm_password', 'email']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("password does not match")
        return confirm


class ownerUpdateModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="confirm password",
        widget=forms.PasswordInput(render_value=True)
    )
    class Meta:
        model = models.User
        fields = ['username', 'password', 'confirm_password', 'email']
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password"))
        if confirm != pwd:
            raise ValidationError("password does not match")
        return confirm

class OrderModelForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = ['destination', 'arrival_time', 'total_passanger', 'vehicle_type', 'shareable', 'special_requests']
        widgets = {
            'arrival_time' : forms.DateTimeInput(attrs={'placeholder': '2006-10-25 14:30:59'})
        }
        

class SharerSearchOrderForm(forms.Form):
    destination = forms.CharField(max_length=100)
    earliestTime = forms.DateTimeField()
    latestTime = forms.DateTimeField()
    number_passengers = forms.IntegerField()


class DriverUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Driver
        fields = ['vehicle_type', 'maxslot', 'plate_number']