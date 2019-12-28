from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


@login_required
def add_profile(request):
    print("REQUEST: ", request.method)
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

        return redirect('webapp:home')

    else:
        print("Erro")
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
    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        type = form.cleaned_data['type']
        user_obj = AppUser.objects.filter(name=name, email=email, phone_number=phone_number,cc=cc,nif=nif,type=type)

        form = RawAppUserForm()
    context = {
        'form' : form ,
        'name' : user_obj
    }
    return render(request, "webapp/search_user.html", context)

