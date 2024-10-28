from django.db import models
from django.core.validators import EmailValidator

class Hospital(models.Model):
    hospital_email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()])  
    name = models.CharField(unique = True,max_length=255) 
    address = models.CharField(max_length=255, null=True, blank=False)
    phone_no = models.CharField(max_length=25, default="Add phone number")

    def __str__(self):
        return self.name  



class Doctor(models.Model):
    doctor_email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()]) 
    license_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    dob = models.DateField()
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name
