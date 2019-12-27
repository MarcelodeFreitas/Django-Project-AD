from django.db import models

class User(models.Model):
    name = models.CharField("Nome",max_length=50)
    username = models.UsernameField("Username", max_length=50, unique=True, default='')
    email = models.EmailField(max_length=256) # A CharField that checks that the value is a valid email address using EmailValidator.
    phone_number = models.CharField("Número de telemóvel", max_length=9)
    cc = models.CharField("Número de cartão de cidadão", max_length=8, unique=True)
    nif = models.CharField("Número de identificação fiscal", max_length=9, unique=True)
    address = models.CharField("Morada", max_length=200)
    cp = models.CharField("Código de postal", max_length=8)
    date = models.DateTimeField(auto_now_add=True) #guarda automaticamente a data a que foi criado

    def __str__(self):
        return str((str(self.name), str(self.cc), str(self.nif), str(self.date)))


class AppUser(User):
    TYPES = [
        ('A', 'Admin'),
        ('M', 'Medic'),
        ('S', 'Secretary'),
    ]
    type = models.CharField("Tipo",max_length=1, choices=TYPES)


class Pacient(User):
    pacient_number = models.CharField("Número de utente", max_length=9, unique=True)
    insurance = models.CharField('Seguro de saúde',max_length=30, blank=True) #blank=True num formulario poderá ser introduzido um valor vazio, ou seja, pode-se deixar em branco

    def __str__(self):
        return str((str(self.name), str(self.cc), str(self.nif), str(self.insurance), str(self.pacient_number), str(self.date)))


class Drug(models.Model):
    name = models.CharField("Nome",max_length=50)
    dci = models.CharField("Denominação comum internacional", max_length=50)
    dosage = models.CharField("Posologia",max_length=10)
    generic = models.BooleanField(verbose_name="Genérico")
    how_to_take = models.CharField("Forma de tomar", max_length=250)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.name), str(self.dci), str(self.dosage), str(self.generic), str(self.how_to_take), str(self.date)))


class Prescription(models.Model):
    medic = models.ForeignKey(AppUser(type='M'),verbose_name="Médico", on_delete=models.PROTECT) #CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(),verbose_name="Paciente", on_delete=models.PROTECT)
    drug = models.ForeignKey(Drug(),verbose_name="Medicamento", on_delete=models.PROTECT)
    aditional_info = models.CharField("Notas", max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.drug), str(self.date)))


class Exam(models.Model):
    medic = models.ForeignKey(AppUser(type='M'), verbose_name="Médico",on_delete=models.PROTECT)  # CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(), verbose_name="Paciente", on_delete=models.PROTECT)
    exam_type = models.CharField("Tipo de exame", max_length=30)
    exam_result = models.URLField(verbose_name="Resultado do exame", blank=True) #será um link para download de um ficheiro
    aditional_info = models.CharField("Notas", max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.exam_type), str(self.exam_result), str(self.date)))


class Appointment(models.Model):
    medic = models.ForeignKey(AppUser(type='M'), verbose_name="Médico", on_delete=models.PROTECT)  # CASCADE vai eliminar a prescrição se o médico for eliminado, PROTECT não vai permitir eliminar médicos que tenham passado prescrições
    pacient = models.ForeignKey(Pacient(), verbose_name="Paciente", on_delete=models.PROTECT)
    aditional_info = models.CharField("Notas", max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str((str(self.medic), str(self.pacient), str(self.date)))
