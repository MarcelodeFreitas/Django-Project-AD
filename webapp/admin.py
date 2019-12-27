from django.contrib import admin

from .models import *


admin.site.register(AppUser)
admin.site.register(Pacient)
admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(Exam)
admin.site.register(Appointment)