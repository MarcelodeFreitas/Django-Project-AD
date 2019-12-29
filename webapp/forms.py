from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput()) #esconde a palavra passe do ecrã

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Incorrect username or password!')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect username or password!')
        return super(LoginForm, self).clean(*args, **kwargs)

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

    def clean_email(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("Passwords must match")
        return password1


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
    phone_number = forms.CharField(max_length=9, required=False)
    cc = forms.CharField(max_length=8, required=False)
    nif = forms.CharField(max_length=9, required=False)
    address = forms.CharField(required=False)
    cp = forms.CharField(max_length=8, required=False)

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
    phone_number = forms.CharField(max_length=9, required=False)
    cc = forms.CharField(max_length=8, required=False)
    nif = forms.CharField(max_length=9, required=False)
    address = forms.CharField(required=False)
    cp = forms.CharField(max_length=8, required=False)
    pacient_number = forms.CharField(max_length=9, required=False)
    insurance = forms.CharField(required=False)


class RawDrugForm(forms.Form):
    name = forms.CharField(required=False)
    dci = forms.CharField(required=False)
    dosage = forms.CharField(required=False)
    generic = forms.BooleanField(required=False)
    how_to_take = forms.CharField(required=False)


class RawAppointmentForm(forms.Form):
    medic_username = forms.CharField()
    pacient_number = forms.CharField(max_length=9)


class RawPrescriptionForm(forms.Form):
    medic_username = forms.CharField()
    pacient_number = forms.CharField(max_length=9)
    drug_id = forms.IntegerField(required=False)


class RawExamForm(forms.Form):
    medic_username = forms.CharField()
    pacient_number = forms.CharField(max_length=9, required=False)
    exam_type = forms.CharField(required=False)
