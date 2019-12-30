import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import *
from django.http import *
from django.core.files.storage import FileSystemStorage


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
            try:
                appuser = AppUser.objects.get(user=request.user)
            except AppUser.DoesNotExist:
                raise Http404('Object Appuser does not exist!')
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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

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

        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()
        messages.success(request, 'User registration succefully')

    else:
        messages.error(request, 'User registration unsuccefully')
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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = PacientForm(request.POST)
    if form.is_valid():
        form.save()
        form = PacientForm()
        messages.success(request, 'Pacient registration succefully')
    else:
        messages.error(request, 'Pacient registration unsuccefully')
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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = DrugForm(request.POST)
    if form.is_valid():
        form.save()
        form = DrugForm()
        messages.success(request, 'Drug registration succefully')
    else:
        messages.error(request, 'Drug registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_drug.html", context)


@login_required
def add_appointment_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = AddAppointmentForm(request.POST)
    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        date_time_start = form.cleaned_data['date_time_start']
        date_time_finish = form.cleaned_data['date_time_finish']
        additional_info = form.cleaned_data['aditional_info']

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object Medic does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                form = AddAppointmentForm()
                raise Http404('Object Medic does not exist!')

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        a = Appointment(medic=medic, pacient=pac, date_time_start=date_time_start,
                         date_time_finish = date_time_finish, aditional_info=additional_info)

        appointments_medic = Appointment.objects.filter(medic=medic)

        b = appointments_medic.filter(date_time_start__range=(date_time_start, date_time_finish)).count()
        print("b:", b)
        c = appointments_medic.filter(date_time_finish__range=(date_time_start, date_time_finish)).count()
        print("c:", c)
        e = appointments_medic.all().filter(date_time_start__lte=date_time_start, date_time_finish__gte=date_time_start)
        print("e:", e)
        f = e.filter(date_time_start__lte= date_time_finish, date_time_finish__gte=date_time_finish).count()
        print("f:", f)

        appointments_pac = Appointment.objects.filter(pacient=pac)

        g = appointments_pac.filter(date_time_start__range=(date_time_start, date_time_finish)).count()
        print("g:", g)
        h = appointments_pac.filter(date_time_finish__range=(date_time_start, date_time_finish)).count()
        print("h:", h)
        i = appointments_pac.all().filter(date_time_start__lte=date_time_start, date_time_finish__gte=date_time_start)
        print("i:", i)
        j = i.filter(date_time_start__lte=date_time_finish, date_time_finish__gte=date_time_finish).count()
        print("j:", j)

        if b != 0:
            messages.error(request, 'Medic not available!')
        elif c != 0:
            messages.error(request, 'Medic not available!')
        elif f != 0:
            messages.error(request, 'Medic not available!')
        elif g != 0:
            messages.error(request, 'Pacient not available!')
        elif h != 0:
            messages.error(request, 'Pacient not available!')
        elif j != 0:
            messages.error(request, 'Pacient not available!')
        else:
            a.save()
            messages.error(request, 'Appointment registration succefully')

        form = AddAppointmentForm()

    else:
        messages.error(request, 'Appointment registration unsuccefully')
    context = {
        'form': form,
        'appuser' : appuser
    }
    return render(request, "webapp/add_appointment.html", context)


@login_required
def add_prescription_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = AddPrescriptionForm(request.POST)
    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        drug_id = form.cleaned_data['drug_id']
        additional_info = form.cleaned_data['aditional_info']

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object Medic does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        if drug_id:
            try:
                drug = Drug.objects.get(id= drug_id)
            except Drug.DoesNotExist:
                raise Http404('Object Drug does not exist!')


        p = Prescription(medic=medic,pacient=pac, drug=drug, aditional_info=additional_info)

        p.save()

        form = AddPrescriptionForm()
        messages.success(request, 'Prescription registration succefully')
    else:
        messages.error(request, 'Prescription registration unsuccefully')
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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = AddExamForm(request.POST)
    if form.is_valid():
        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        exam_type = form.cleaned_data['exam_type']
        additional_info = form.cleaned_data['aditional_info']

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object Medic does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Medic does not exist!')



        e = Exam(medic=medic, pacient=pac, exam_type=exam_type, aditional_info=additional_info)

        e.save()

        form = AddExamForm()
        messages.success(request, 'Exam registration succefully')
    else:
        messages.error(request, 'Exam registration unsuccefully')
    context = {
        'form': form,
        'appuser': appuser
    }
    return render(request, "webapp/add_exam.html", context)


@login_required
def search_user_view(request):

    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawAppointmentForm(request.POST or None)
    obj = Appointment.objects.all()

    if form.is_valid():
        med = None
        pac = None

        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        date_time_search = form.cleaned_data['date_time_search']

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Pacient does not exist!')

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object User does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if date_time_search:
            obj = obj.filter(date_time_start__gte=date_time_search, date_time_finish__lte=date_time_search)

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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawPrescriptionForm(request.POST)
    obj = None

    if form.is_valid():
        med = None
        pac = None
        drug_id = None

        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        drug_id = form.cleaned_data['drug_id']

        if drug_id:
            try:
                drug = Drug.objects.get(id=drug_id)
            except Drug.DoesNotExist:
                raise Http404('Object Drug does not exist!')

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Pacient does not exist!')

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object User does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                raise Http404('Object Medic does not exist!')

        obj = Prescription.objects.all()
        print(obj)

        if med:
            obj = obj.filter(medic=med)
        if pac:
            obj = obj.filter(pacient=pac)
        if drug_id:
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
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = RawExamForm(request.POST or None)
    obj = Exam.objects.all()

    if form.is_valid():
        med = None
        pac = None

        medic_username = form.cleaned_data['medic_username']
        pacient_number = form.cleaned_data['pacient_number']
        exam_type = form.cleaned_data['exam_type']

        if pacient_number:
            try:
                pac = Pacient.objects.get(pacient_number=pacient_number)
            except Pacient.DoesNotExist:
                raise Http404('Object Pacient does not exist!')

        if medic_username:
            try:
                user = User.objects.get(username=medic_username)
            except User.DoesNotExist:
                raise Http404('Object User does not exist!')
            try:
                medic = AppUser.objects.get(user=user, type='M')
                if medic.type != 'M':
                    raise Http404('Username does not belong to a Medic!')
            except AppUser.DoesNotExist:
                raise Http404('Object Medic does not exist!')

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


@login_required
def upload_users_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        title = form.cleaned_data['title']
        txt = form.cleaned_data['txt']

        Upload.objects.create(user=request.user, title=title, txt=txt)



        print("txt", txt)
        print("txt.open()",txt.open())


        read = txt.read()
        print(read)

        decoded = read.decode()
        print(decoded)

        line = decoded.split("\r\n")

        print("line", line)

        i = 0
        while i < len(line):
            arg_list = line[i].split(":")
            username = arg_list[0]
            password1 = arg_list[1]
            password2 = arg_list[2]
            name = arg_list[3]
            email = arg_list[4]
            phone_number = arg_list[5]
            cc = arg_list[6]
            nif = arg_list[7]
            address = arg_list[8]
            pc = arg_list[9]
            type = arg_list[10]
            print("username", username)
            print("password1", password1)
            print("password2", password2)
            print("name", name)
            print("email", email)
            print("phone", phone_number)
            print("cc", cc)
            print("nif", nif)
            print("address", address)
            print("pc", pc)
            print("type", type)
            i += 1

            user = User.objects.create(username=username, password=password1)
            print("USER: ", user)

            profile = AppUser.objects.create(user=user, name=name, email=email, phone_number=phone_number,
                                             cc=cc, nif=nif, address=address, cp=pc, type=type)

            print("PROFILE: ", profile)

            if type == 'A':
                user = User.objects.get(username=username)
                mygroup, created = Group.objects.get_or_create(name='Admin')
                mygroup.user_set.add(user)
                mygroup.save()

            if type == 'M':
                user = User.objects.get(username=username)
                mygroup, created = Group.objects.get_or_create(name='Medic')
                mygroup.user_set.add(user)
                mygroup.save()

            if type == 'S':
                user = User.objects.get(username=username)
                mygroup, created = Group.objects.get_or_create(name='Secretary')
                mygroup.user_set.add(user)
                mygroup.save()

        messages.success(request, 'File upload succesfull! Users added!')

    else:
        messages.error(request, 'File upload unsuccefully! Users not added!')
        form = UploadForm()
    context = {
        'form': form,
    }
    return render(request, 'webapp/upload_users.html', context)


@login_required
def upload_pacients_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        title = form.cleaned_data['title']
        txt = form.cleaned_data['txt']

        Upload.objects.create(user=request.user, title=title, txt=txt)

        print("txt", txt)
        print("txt.open()",txt.open())

        read = txt.read()
        print(read)

        decoded = read.decode()
        print(decoded)

        line = decoded.split("\r\n")

        print("line", line)

        i = 0
        while i < len(line):
            arg_list = line[i].split(":")
            name = arg_list[0]
            email = arg_list[1]
            phone_number = arg_list[2]
            cc = arg_list[3]
            nif = arg_list[4]
            address = arg_list[5]
            pc = arg_list[6]
            pacient_number = arg_list[7]
            insurance = arg_list[8]

            print("name", name)
            print("email", email)
            print("phone", phone_number)
            print("cc", cc)
            print("nif", nif)
            print("address", address)
            print("pc", pc)
            print("pacient_number", pacient_number)
            print("insurance", insurance)
            i += 1

            Pacient.objects.create(name=name, email=email, phone_number=phone_number,
                                   cc=cc, nif=nif, address=address, cp=pc, pacient_number=pacient_number,
                                   insurance=insurance)

        messages.success(request, 'File upload succesfull! Pacients added!')

    else:
        messages.error(request, 'File upload unsuccefully! Pacients not added!')
        form = UploadForm()
    context = {
        'form': form,
    }
    return render(request, 'webapp/upload_pacients.html', context)

@login_required
def upload_drugs_view(request):
    appuser = None
    if request.user.is_superuser:
        appuser = None
    elif request.user.is_authenticated:
        try:
            appuser = AppUser.objects.get(user=request.user)
        except AppUser.DoesNotExist:
            raise Http404('Object Appuser does not exist!')

    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        title = form.cleaned_data['title']
        txt = form.cleaned_data['txt']

        Upload.objects.create(user=request.user, title=title, txt=txt)


        txt.open()

        read = txt.read()

        decoded = read.decode()

        line = decoded.split("\r\n")

        i = 0
        while i < len(line):
            arg_list = line[i].split(";")
            name = arg_list[0]
            dci = arg_list[1]
            dosage = arg_list[2]
            generic = arg_list[3]
            how_to_take = arg_list[4]
            i += 1

            Drug.objects.create(name=name, dci=dci, dosage=dosage, generic=generic, how_to_take=how_to_take)

        messages.success(request, 'File upload succesfull! Drugs added!')

    else:
        messages.error(request, 'File upload unsuccefully! Drugs not added!')
        form = UploadForm()
    context = {
        'form': form,
    }
    return render(request, 'webapp/upload_drugs.html', context)

