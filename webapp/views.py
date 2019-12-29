from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import *
from django.http import HttpResponse

@login_required
def add_profile(request):
    print(request.method)
    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserProfileForm(request.POST or None)

    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        print("USER: ",user)
        profile = profile_form.save(commit=False)

        profile.user = user
        print("PROFILE: ", profile)
        profile.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)

        type = profile_form.cleaned_data.get('type')

        if type == 'A':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Admin')
            mygroup.user_set.add(user)
            mygroup.save()

        if type == 'M':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Medic')
            mygroup.user_set.add(user)
            mygroup.save()

        if type == 'S':
            user = User.objects.get(username=form.cleaned_data.get('username'))
            mygroup, created = Group.objects.get_or_create(name='Secretary')
            mygroup.user_set.add(user)
            mygroup.save()

        return redirect('webapp:home')

    else:
        print("Invalid field, please try again!")

        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form': profile_form}

    return render(request, "webapp/add_profile.html", context)


def home(request):
    return render(request, "webapp/index.html", {})


@login_required
def add_pacient_view(request):
    form = PacientForm(request.POST)
    if form.is_valid():
        form.save()
        form = PacientForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_pacient.html", context)


@login_required
def add_drug_view(request):
    form = DrugForm(request.POST)
    if form.is_valid():
        form.save()
        form = DrugForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_drug.html", context)


@login_required
def add_exam_view(request):
    form = ExamForm(request.POST)
    if form.is_valid():
        form.save()
        form = ExamForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_exam.html", context)


@login_required
def add_prescription_view(request):
    form = PrescriptionForm(request.POST)
    if form.is_valid():
        form.save()
        form = PrescriptionForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_prescription.html", context)


@login_required
def add_appointment_view(request):
    form = AppointmentForm(request.POST)
    if form.is_valid():
        form.save()
        form = AppointmentForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_appointment.html", context)


@login_required
def search_user_view(request):
    form = RawAppUserForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        type = form.cleaned_data['type']
        obj = AppUser.objects.all()

        if name:
            obj = obj.filter(name=name)
        if email:
            obj = obj.filter(email=email)
        if phone_number:
            obj = obj.filter(phone_number=phone_number)
        if cc:
            obj = obj.filter(cc=cc)
        if nif:
            obj = obj.filter(nif=nif)
        if type=='NONE':
            type = None
        if type:
            obj = obj.filter(type=type)

        form = RawAppUserForm()
    context = {
        'form' : form ,
        'obj' : obj
    }
    return render(request, "webapp/search_user.html", context)


@login_required
def search_pacient_view(request):
    form = RawPacientForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        pacient_number = form.cleaned_data['pacient_number']
        insurance = form.cleaned_data['insurance']
        obj = Pacient.objects.all()

        if name:
            obj = obj.filter(name=name)
        if email:
            obj = obj.filter(email=email)
        if phone_number:
            obj = obj.filter(phone_number=phone_number)
        if cc:
            obj = obj.filter(cc=cc)
        if nif:
            obj = obj.filter(nif=nif)
        if pacient_number:
            obj = obj.filter(pacient_number=pacient_number)
        if insurance:
            obj = obj.filter(insurance=insurance)

        form = RawPacientForm()
    context = {
        'form' : form ,
        'obj' : obj
    }
    return render(request, "webapp/search_pacient.html", context)


@login_required
def search_drug_view(request):
    form = RawDrugForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        dci = form.cleaned_data['dci']
        dosage = form.cleaned_data['dosage']
        generic = form.cleaned_data['generic']
        how_to_take = form.cleaned_data['how_to_take']
        obj = Drug.objects.all()

        if name:
            obj = obj.filter(name=name)
        if dci:
            obj = obj.filter(dci=dci)
        if dosage:
            obj = obj.filter(dosage=dosage)
        if generic:
            obj = obj.filter(generic=generic)
        if how_to_take:
            obj = obj.filter(how_to_take=how_to_take)

        form = RawDrugForm()
    context = {
        'form' : form ,
        'obj' : obj
    }
    return render(request, "webapp/search_drug.html", context)


@login_required
def search_prescription_view(request):
    form = RawPrescriptionForm(request.POST)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']

        user = User.objects.get(username=medic_username)
        med = AppUser.objects.get(user=user)
        obj = Prescription.objects.all()

        if med:
            obj = obj.filter(med=med)

        form = RawDrugForm()
    context = {
        'form' : form ,
        'obj' : obj
    }
    return render(request, "webapp/search_prescription.html", context)