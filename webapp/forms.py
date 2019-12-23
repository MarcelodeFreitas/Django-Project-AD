from django import forms

from .models import *

class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = [
            'name',
            'type',
            'email',
            'phone_number',
            'cc',
            'nif',
            'address',
            'cp'
        ]