from django.contrib import admin

from .models import *
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Donor)
admin.site.register(Organ)
admin.site.register(parts)
admin.site.register(Patient)
admin.site.register(Request)
admin.site.register(Appointments)
admin.site.register(Appointments_request)


