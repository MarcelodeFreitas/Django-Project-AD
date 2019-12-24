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

def auth(request):
    return render(request, "webapp/auth.html")

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
    context = {'form' : form}
    return render(request, 'registration/register.html', context)

# pode-se alterar o UserCreationForm, criando o form.py,
# cria-se uma nova classe extende-se o UserCreationForm
# e adiciona-se os campos adicionais