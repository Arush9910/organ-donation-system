from django.db import models
from django.core.validators import EmailValidator

class Hospital(models.Model):
    hospital_email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()])  
    name = models.CharField(unique = True,max_length=255) 
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_no = models.CharField(max_length=25, default="Add phone number")
    pic = models.ImageField(upload_to = "pictures",null=True,blank = True)

    def __str__(self):
        return self.name  



class Doctor(models.Model):
    doctor_email = models.EmailField(max_length=254, unique=True, validators=[EmailValidator()]) 
    license_no = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    dob = models.DateField()
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=400,null = True , blank=True)
    pic = models.ImageField(upload_to = "pictures",null=True,blank = True)


    def __str__(self):
        return self.name





class Donor(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    ORGAN_CHOICES = [
        ('All Organs', 'All Organs'),
        ('Corneas (Eyes)', 'Corneas (Eyes)'),
        ('Kidneys', 'Kidneys'),
        ('Heart', 'Heart'),
        ('Lungs', 'Lungs'),
        ('Liver', 'Liver'),
        ('Pancreas', 'Pancreas'),
        ('Small Intestine', 'Small Intestine'),
        ('Skin', 'Skin'),
        ('Hands', 'Hands'),
    ]
    
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    pin_code = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def _str_(self):
        return self.full_name
    
class parts(models.Model):
    donor_id=models.ForeignKey(Donor, on_delete=models.SET_NULL, null=True, blank=True)
    parts=models.CharField(max_length=100)
    
class Organ(models.Model):
    organ_name = models.CharField(max_length=150) 
    donor_name = models.CharField(max_length=150)  
    donor_age = models.PositiveIntegerField()
    blood_group = models.CharField(max_length=150)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return f"{self.organ_name} from {self.donor_name}"
    


class Patient(models.Model):
    patient_name = models.CharField(max_length = 250)
    patient_age = models.IntegerField()
    patient_gender = models.CharField(max_length = 150)
    hospital = models.ForeignKey(Hospital,on_delete = models.SET_NULL, null=True,blank = True)
    doctor = models.ForeignKey(Doctor,on_delete = models.SET_NULL,null = True, blank = True)
    