from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


def add_appuser_view(request):
    form = AppUserForm(request.POST)
    if form.is_valid():
        form.save()
        form = AppUserForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_appuser.html", context)


def home(request):
    return render(request, "webapp/index.html", {})


def add_pacient_view(request):
    form = PacientForm(request.POST)
    if form.is_valid():
        form.save()
        form = PacientForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_pacient.html", context)


def add_drug_view(request):
    form = DrugForm(request.POST)
    if form.is_valid():
        form.save()
        form = DrugForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_drug.html", context)


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



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('webapp:home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/register.html', context)

# pode-se alterar o UserCreationForm, criando o form.py,
# cria-se uma nova classe extende-se o UserCreationForm
# e adiciona-se os campos adicionais