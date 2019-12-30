from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField("Name",max_length=50)
    email = models.EmailField(max_length=256) # A CharField that checks that the value is a valid email address using EmailValidator.
    phone_number = models.CharField("Phone Number", max_length=9)
    cc = models.CharField("CC", max_length=8, unique=True)
    nif = models.CharField("NIF", max_length=9, unique=True)
    address = models.CharField("Address", max_length=200)
    cp = models.CharField("Postal Code", max_length=8)
    date = models.DateTimeField(auto_now_add=True) #guarda automaticamente a data a que foi criado

    def __str__(self):
        return str((str(self.name), str(self.type)))


class AppUser(Profile):
    TYPES = [
        ('A', 'Admin'),
        ('M', 'Medic'),
        ('S', 'Secretary'),
    ]
    type = models.CharField("Type",max_length=1, choices=TYPES)


class Pacient(models.Model):
    name = models.CharField("Name", max_length=50)
    email = models.EmailField(max_length=256)  # A CharField that checks that the value is a valid email address using EmailValidator.
    phone_number = models.CharField("Phone Number", max_length=9)
    cc = models.CharField("CC", max_length=8, unique=True)
    nif = models.CharField("NIF", max_length=9, unique=True)
    address = models.CharField("Address", max_length=200)
    cp = models.CharField("Postal Code", max_length=8)
    date = models.DateTimeField(auto_now_add=True)  # guarda automaticamente a data a que foi criado
    pacient_number = models.CharField("Pacient Number", max_length=9, unique=True)
    insurance = models.CharField('Insurance',max_length=30, blank=True) #blank=True num formulario poderá ser introduzido um valor vazio, ou seja, pode-se deixar em branco

    def __str__(self):
        return str((str(self.name), str(self.pacient_number), str(self.insurance)))


class Drug(models.Model):
    name = models.CharField("Name",max_length=50)
    dci = models.CharField("DCI", max_length=50)
    dosage = models.CharField("Dosage",max_length=10)
    generic = models.BooleanField(verbose_name="Generic")
    how_to_take = models.CharField("How to take", max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.name), str(self.dci), str(self.dosage), str(self.generic), str(self.how_to_take), str(self.date)))


class Appointment(models.Model):
    medic = models.ForeignKey(AppUser(type='M'), verbose_name="Medic", on_delete=models.PROTECT)  # CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(), verbose_name="Pacient", on_delete=models.PROTECT)
    aditional_info = models.TextField("Notes", max_length=500, blank=True)
    date_time_start = models.DateTimeField(null=False, blank=False)
    date_time_finish = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.date)))


class Prescription(models.Model):
    medic = models.ForeignKey(AppUser(type='M'),verbose_name="Medic", on_delete=models.PROTECT) #CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(),verbose_name="Pacient", on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug(),verbose_name="Drug", on_delete=models.PROTECT)
    aditional_info = models.TextField("Notes", max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.drug), str(self.date)))


class Exam(models.Model):
    medic = models.ForeignKey(AppUser(type='M'), verbose_name="Medic",on_delete=models.PROTECT)  # CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(), verbose_name="Pacient", on_delete=models.PROTECT)
    exam_type = models.CharField("Type of exam", max_length=30)
    exam_result = models.URLField(verbose_name="Result of exam", blank=True) #será um link para download de um ficheiro
    aditional_info = models.TextField("Notes", max_length=500, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.exam_type), str(self.exam_result), str(self.date)))




