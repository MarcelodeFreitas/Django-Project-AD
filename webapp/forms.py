from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput()) #esconde a palavra passe do ecrã

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



class RawAppUserForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    cc = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    address = forms.CharField(required=False)
    cp = forms.CharField(required=False)

    TYPES = [
        ('NONE', '-'),
        ('A', 'Admin'),
        ('M', 'Medic'),
        ('S', 'Secretary'),
    ]

    type = forms.ChoiceField(required=False, choices=TYPES)


class RawPacientForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)
    cc = forms.CharField(required=False)
    nif = forms.CharField(required=False)
    address = forms.CharField(required=False)
    cp = forms.CharField(required=False)
    pacient_number = forms.CharField(required=False)
    insurance = forms.CharField(required=False)


class RawDrugForm(forms.Form):
    name = forms.CharField(required=False)
    dci = forms.CharField(required=False)
    dosage = forms.CharField(required=False)
    generic = forms.BooleanField(required=False)
    how_to_take = forms.CharField(required=False)


class RawPrescriptionForm(forms.Form):
    medic_username = forms.CharField()
    pacient_number = forms.CharField(max_length=9)
    drug_id = forms.IntegerField()
    date = forms.DateTimeField()

class RawExamForm(forms.Form):
    medic_username = forms.CharField()
    pacient_number = forms.CharField(max_length=9)
    exam_type = forms.CharField
    date = forms.DateTimeField()


class RawAppointmentForm(forms.Form):
    name = forms.CharField(required=False)
    dci = forms.CharField(required=False)
    dosage = forms.CharField(required=False)
    generic = forms.BooleanField(required=False)
    how_to_take = forms.CharField(required=False)




