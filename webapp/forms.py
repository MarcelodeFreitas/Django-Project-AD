from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ExtendedUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data['username']

        if commit:
            user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = [
            'name',
            'email',
            'phone_number',
            'cc',
            'nif',
            'address',
            'cp',
            'type'
        ]


'''class AppUserForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = '__all__'''


class PacientForm(forms.ModelForm):
    class Meta:
        model = Pacient
        fields = [
            'name',
            'email',
            'phone_number',
            'cc',
            'nif',
            'address',
            'cp',
            'pacient_number',
            'insurance',
        ]


class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = '__all__'


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'



'''class RawAppUserForm(forms.Form):
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

    type = forms.ChoiceField(required=True, choices=TYPES)'''



