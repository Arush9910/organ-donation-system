from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils import timezone
from tables.models import Hospital, Doctor ,Organ ,Patient# Import models explicitly
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, "hello.html")

def log_in(request):
    if request.method == "POST":
        data = request.POST
        u = data.get('username')
        p = data.get('password')

        if User.objects.filter(username=u).exists():
            user = User.objects.get(username=u)
            if check_password(p, user.password):
                try:
                    h = Hospital.objects.get(hospital_email = u)

                    return redirect(f'/hospital_dashboard/{h.id}')  
                except Hospital.DoesNotExist:

                    try:
                        d = Doctor.objects.get(doctor_email = u)
                        return redirect('/doctor')
                    except Doctor.DoesNotExist:

                        ''' NEED TO CHECK FOR DONOR USING ANOTHER EXCEPTINO CATCHING NEED TO MAKE TABLE AND HTMOL FOR THAT'''
                        pass
            else:
                messages.error(request,'Invalid Password')
        else:
            messages.error(request,'Invalid Username')





#loginrequired need to add


                 
                

    return render(request, "login.html")

@login_required
def hosp_doc(request):
    return render(request, 'hospital-doctors.html')  

def pledge(request):
    return render(request, 'pledge.html')

def signupd(request):

    if request.method == "POST":
        data = request.POST
        name = data.get('name')
        dob = data.get('dob')
        phone_no = data.get('phone_no')
        license_no = data.get('license_no')
        hospital = data.get('hospital')
        password = data.get('password')
        email = data.get('email')
        
        

        try:
           h = Hospital.objects.get(name=hospital)  
        except Hospital.DoesNotExist:  
           messages.error(request, 'Hospital name is incorrect')
           return redirect('/signupd')
        
        try:
            d = Doctor.objects.get(doctor_email = email)
            messages.error(request,'email is already in use')
            return redirect('/signupd')
        except Doctor.DoesNotExist:
            pass

        d = Doctor.objects.create(
            name=name,
            dob=dob,
            phone_no=phone_no,
            license_no=license_no,
            hospital=h,
            doctor_email=email,
        )
        

        u = User.objects.create(
            first_name = name,
            last_name = name,
            username = email,
        )
        u.set_password(password)
        u.save()

        messages.info(request,'account created succesfully')
        return redirect('/login')

    return render(request, 'signupd.html')


def hospital_dashboard(request,id):

    hospital_info = Hospital.objects.get(id = id)
    pateint_info = Patient.objects.filter(hospital = id)
    organ_info = Organ.objects.filter(hospital = id)
    doctor_info = Doctor.objects.filter(hospital = id)
    patient_no = pateint_info.count()
    organ_no = organ_info.count()
    doctor_no = doctor_info.count()



    return render(request,'hospital.html',context = {'id':id , 'hospital_info': hospital_info,'organ_no':organ_no,'patient_no':patient_no,'doctor_no':doctor_no})

def hospital_doctors(request,id):
    hospital_info = Hospital.objects.get(id = id)
    doctor_info = Doctor.objects.filter(hospital = id)
    return render(request,'hospital-doctors.html',context = {'id':id,'hospital_info': hospital_info,'doctor_info':doctor_info})

def hospital_organs(request,id):
    hospital_info = Hospital.objects.get(id = id)
    organ_info = Organ.objects.filter(hospital = hospital_info.id)
    return render(request,'hospital-organs.html',context = {'id':id,'hospital_info': hospital_info,'organ_info': organ_info})

def hospital_patients(request,id):
    hospital_info = Hospital.objects.get(id = id)
    patient_info = Patient.objects.filter(hospital = hospital_info.id)
    doctor_info = Doctor.objects.all()
    return render(request,'hospital-patients.html',context = {'id':id , 'hospital_info': hospital_info,'patient_info':patient_info,'doctor_info':doctor_info})

def remove_doctor_from_hospital(request,id,email):
    doctor_to_be_removed =  Doctor.objects.get(doctor_email = email)
    doctor_to_be_removed.delete()
    return redirect(f'/hospital_doctors/{id}')

def remove_organ_from_hospital(request,id,organ_id):
    organ_to_be_removed = Organ.objects.get(id = organ_id)
    organ_to_be_removed.delete()
    return redirect(f'/hospital_organs/{id}')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def profile(request):
    return render(request,'profile.html')
    
        

