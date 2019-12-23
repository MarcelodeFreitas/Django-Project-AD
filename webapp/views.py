from .forms import *
from .models import *
from django.shortcuts import render

def add_appuser_view(request):
    form = AppUserForm(request.POST)
    if form.is_valid():
        form.save()
        form = AppUserForm()
    context = {
        'form': form
    }
    return render(request, "webapp/add_appuser.html", context)