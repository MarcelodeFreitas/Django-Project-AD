from django import forms

from .models import *

class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'


class PacientForm(forms.ModelForm):
    class Meta:
        model = Pacient
        fields = '__all__'

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'

class RawAppUserForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    cc = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    address = forms.CharField(required=False)
    cp = forms.CharField(required=False)

    TYPES = [
        ('A', 'Admin'),
        ('M', 'Medic'),
        ('S', 'Secretary'),
    ]

    type = forms.ChoiceField(required=True, choices=TYPES)



