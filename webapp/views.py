from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import *
from django.http import HttpResponse


def login_view(request):
    user = None
    app_user = None
    message = None
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        #print(user.is_superuser)
        if user.is_superuser:
            login(request, user)
            return redirect('webapp:home')
        else:
            if user is not None:
                app_user = AppUser.objects.get(user=user)
                login(request, user)
                return redirect('webapp:home')

    context = {
        'form': form,
        'user': user,
        'appuser': app_user,
    }
    return render(request, "webapp/login.html", context)

def logout_view(request):
    logout(request)
    return redirect('webapp:login')


def home_view(request):
    if request.user.is_superuser:
        context = {}
    else :
        if request.user.is_authenticated:
            appuser = AppUser.objects.get(user=request.user)
            context = {
                'appuser' : appuser
            }
    return render(request, "webapp/index.html", context)

@login_required
def add_profile_view(request):
    print(request.method)

    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = ExtendedUserCreationForm(request.POST or None)
    profile_form = UserProfileForm(request.POST or None)

    if form.is_valid() and profile_form.is_valid():
        user = form.save()
        print("USER: ",user)
        profile = profile_form.save(commit=False)

        profile.user = user
        print("PROFILE: ", profile)
        profile.save()

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

    context = {
        'form': form,
        'profile_form': profile_form,
        'appuser': appuser
    }

    return render(request, "webapp/add_profile.html", context)


@login_required
def add_pacient_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = PacientForm(request.POST)
    if form.is_valid():
        form.save()
        form = PacientForm()
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_pacient.html", context)


@login_required
def add_drug_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = DrugForm(request.POST)
    if form.is_valid():
        form.save()
        form = DrugForm()
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_drug.html", context)


@login_required
def add_prescription_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = PrescriptionForm(request.POST)
    if form.is_valid():
        form.save()
        form = PrescriptionForm()
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_prescription.html", context)

@login_required
def add_exam_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = ExamForm(request.POST)
    if form.is_valid():
        form.save()
        form = ExamForm()
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_exam.html", context)


@login_required
def add_appointment_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = AppointmentForm(request.POST)
    if form.is_valid():
        form.save()
        form = AppointmentForm()
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_appointment.html", context)


@login_required
def search_user_view(request):

    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = RawAppUserForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        address = form.cleaned_data['address']
        cp = form.cleaned_data['cp']
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
        if address:
            obj = obj.filter(address=address)
        if cp:
            obj = obj.filter(cp=cp)
        if type=='NONE':
            type = None
        if type:
            obj = obj.filter(type=type)

        form = RawAppUserForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_user.html", context)


@login_required
def search_pacient_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = RawPacientForm(request.POST)
    obj = None

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone_number = form.cleaned_data['phone_number']
        cc = form.cleaned_data['cc']
        nif = form.cleaned_data['nif']
        address = form.cleaned_data['address']
        cp = form.cleaned_data['cp']
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
        if address:
            obj = obj.filter(address=address)
        if cp:
            obj = obj.filter(cp=cp)
        if pacient_number:
            obj = obj.filter(pacient_number=pacient_number)
        if insurance:
            obj = obj.filter(insurance=insurance)

        form = RawPacientForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_pacient.html", context)


@login_required
def search_drug_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

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
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_drug.html", context)


@login_required
def search_appointment_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = RawAppointmentForm(request.POST or None)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']

        pac = Pacient.objects.get(pacient_number=pacient_number)
        user = User.objects.get(username=medic_username)
        med = AppUser.objects.get(user=user)

        obj = Appointment.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)

        form = RawAppointmentForm()

    context = {
        'form': form,
        'obj': obj,
        'appuser': appuser
    }
    return render(request, "webapp/search_appointment.html", context)


@login_required
def search_prescription_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = RawPrescriptionForm(request.POST)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        drug_id = form.cleaned_data['drug_id']

        drug = Drug.objects.get(id=drug_id)
        pac = Pacient.objects.get(pacient_number=pacient_number)
        user = User.objects.get(username=medic_username)
        med = AppUser.objects.get(user=user)

        obj = Prescription.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if drug:
            obj = obj.filter(drug=drug)

        form = RawPrescriptionForm()
    context = {
        'form' : form ,
        'obj' : obj,
        'appuser' : appuser
    }
    return render(request, "webapp/search_prescription.html", context)


@login_required
def search_exam_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        appuser = AppUser.objects.get(user=request.user)

    form = RawExamForm(request.POST or None)
    obj = None

    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        exam_type = form.cleaned_data['exam_type']

        pac = Pacient.objects.get(pacient_number=pacient_number)
        user = User.objects.get(username=medic_username)
        med = AppUser.objects.get(user=user)

        obj = Exam.objects.all()

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if exam_type:
            obj = obj.filter(exam_type=exam_type)

        form = RawExamForm()

    context = {
        'form': form,
        'obj': obj,
        'appuser': appuser
    }
    return render(request, "webapp/search_exam.html", context)