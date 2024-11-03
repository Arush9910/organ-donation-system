from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils import timezone
from tables.models import Hospital, Doctor ,Organ ,Patient,Appointments,Request,Appointments_request,Request,Donor# Import models explicitly
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

def home(request):
    logout(request)
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
                    login(request,user)

                    return redirect(f'/hospital_dashboard/{h.id}')  
                except Hospital.DoesNotExist:

                    try:
                        d = Doctor.objects.get(doctor_email = u)
                        login(request,user)
                        return redirect(f'/doctor_dashboard/{d.id}')
                    except Doctor.DoesNotExist:
                        pass
            else:
                messages.error(request,'Invalid Password')
        else:
            messages.error(request,'Invalid Username')





                 
                

    return render(request, "login.html")


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

        messages.success(request,'account created succesfully')
        return redirect('/login')

    return render(request, 'signupd.html')
@login_required
def hospital_dashboard(request,id):

    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    
    pateint_info = Patient.objects.filter(hospital = id)
    organ_info = Organ.objects.filter(hospital = id)
    doctor_info = Doctor.objects.filter(hospital = id)
    patient_no = pateint_info.count()
    organ_no = organ_info.count()
    doctor_no = doctor_info.count()



    return render(request,'hospital.html',context = {'id':id , 'hospital_info': hospital_info,'organ_no':organ_no,'patient_no':patient_no,'doctor_no':doctor_no})
@login_required
def hospital_doctors(request,id):
    
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    

    doctor_info = Doctor.objects.filter(hospital = id)
    return render(request,'hospital-doctors.html',context = {'id':id,'hospital_info': hospital_info,'doctor_info':doctor_info})
@login_required
def hospital_organs(request,id):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    

    organ_info = Organ.objects.filter(hospital = hospital_info.id)
    return render(request,'hospital-organs.html',context = {'id':id,'hospital_info': hospital_info,'organ_info': organ_info})
@login_required
def hospital_patients(request,id):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    

    patient_info = Patient.objects.filter(hospital = hospital_info.id)
    doctor_info = Doctor.objects.all()
    return render(request,'hospital-patients.html',context = {'id':id , 'hospital_info': hospital_info,'patient_info':patient_info,'doctor_info':doctor_info})
@login_required
def remove_doctor_from_hospital(request,id,email):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    
    doctor_to_be_removed =  Doctor.objects.get(doctor_email = email)
    doctor_to_be_removed.delete()
    return redirect(f'/hospital_doctors/{id}')
@login_required
def remove_organ_from_hospital(request,id,organ_id):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    

    organ_to_be_removed = Organ.objects.get(id = organ_id)
    organ_to_be_removed.delete()
    return redirect(f'/hospital_organs/{id}')

def about(request):
    logout(request)
    return render(request,'about.html')

def contact(request):
    logout(request)
    return render(request,'contact.html')

@login_required
def profile(request,type,id):
    
    
    if request.method == "POST":
        img = request.FILES.get('omg')
        if type == 'Hospital':
            profile = Hospital.objects.get(id = id)
            profile.pic = img
            profile.save()
        else:
            profile = Doctor.objects.get(id = id)
            profile.pic = img
            profile.save()

    
    
    
    if type == 'Hospital':
        hospital_info = Hospital.objects.get(id = id)

        if not request.user.username == hospital_info.hospital_email:
          messages.error(request, "You do not have permission to access this dashboard.")
          return redirect('/login')
    
        profile = Hospital.objects.get(id = id)
        link = f'hospital_dashboard/{id}'
        profile_info = {'id':id,'type':'Hospital','pic':profile.pic,'Name':profile.name,'Email':profile.hospital_email,'Address':profile.address,'Phone_no':profile.phone_no,'link':link}
        
    else:
        doctor_info = Doctor.objects.get(id = id)

        if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')
    
        print("type")
        print(type)
        profile = Doctor.objects.get(id = id)
        profile_info = {'id':id,'type':'Doctor','pic':profile.pic,'Name':profile.name,'Email':profile.doctor_email,'Address':profile.address,'Phone_no':profile.phone_no}
    
    return render(request,'profile.html',context = {'profile_info':profile_info})

@login_required
def profile_edit(request,type,id):
    #type and id check authentication

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        if form_type == "form1":
            img = request.FILES.get('omg')
            if type == 'Hospital':
              profile = Hospital.objects.get(id = id)
              profile.pic = img
              profile.save()
            else:
              profile = Doctor.objects.get(id = id)
              profile.pic = img
              profile.save()


        else:
            Name = request.POST.get('Name')
            Email = request.POST.get('Email')
            Phone_no = request.POST.get('Phone_no')
            Address = request.POST.get('Address')
            if type == 'Hospital':
              
              hospital_info = Hospital.objects.get(id = id)

              if not request.user.username == hospital_info.hospital_email:
                  messages.error(request, "You do not have permission to access this dashboard.")
                  return redirect('/login')
    
              profile = Hospital.objects.get(id = id)
              profile.name = Name
              print('profile',profile.hospital_email)
              user = User.objects.get(username = profile.hospital_email)
              profile.hospital_email = Email
              user.username = profile.hospital_email
              user.save()
              profile.address = Address
              profile.phone_no = Phone_no
              profile.save()
              return redirect(f'/profile/{type}/{id}')
            else:
              doctor_info = Doctor.objects.get(id = id)

              if not request.user.username == doctor_info.doctor_email:
                   messages.error(request, "You do not have permission to access this dashboard.")
                   return redirect('/login')
              
              
              profile = Doctor.objects.get(id = id)
              profile.name = Name
              user = User.objects.get(username = profile.doctor_email)

              profile.doctor_email = Email
              
              user.username = profile.doctor_email

              user.save()
              profile.address = Address
              profile.phone_no = Phone_no
              profile.save()
              return redirect(f'/profile/{type}/{id}')
            

        


    if type == 'Hospital':
        profile = Hospital.objects.get(id = id)
        link = f'hospital_dashboard/{id}'
        profile_info = {'id':id,'type':'Hospital','pic':profile.pic,'Name':profile.name,'Email':profile.hospital_email,'Address':profile.address,'Phone_no':profile.phone_no,'link':link}
        
    else:
        profile = Doctor.objects.get(id = id)
        profile_info = {'id':id,'type':'Doctor','pic':profile.pic,'Name':profile.name,'Email':profile.doctor_email,'Address':profile.address,'Phone_no':profile.phone_no}
    
    return render(request,'profile-edit.html',context = {'profile_info':profile_info})

@login_required
def profile_change(request,type,id):
    flag = -1
    if request.method == "POST":
        Curr = request.POST.get('current_password')
        new = request.POST.get('new_password')
        renew = request.POST.get('confirm_password')
        if type == "Hospital":
            hospital_info = Hospital.objects.get(id = id)

            if not request.user.username == hospital_info.hospital_email:
                messages.error(request, "You do not have permission to access this dashboard.")
                return redirect('/login')
    
            em = Hospital.objects.get(id = id).hospital_email
        else:
            doctor_info = Doctor.objects.get(id = id)

            if not request.user.username == doctor_info.doctor_email:
              messages.error(request, "You do not have permission to access this dashboard.")
              return redirect('/login')
            em = Doctor.objects.get(id = id).doctor_email

        user = User.objects.get(username = em)
        if check_password(Curr,user.password):
            if new == renew:
                
                user.set_password(new)
                user.save()
                flag = 0
            else:
                messages.error(request,'Passwords does not match')
                flag = 1

        else:
            messages.error(request,'Password incorrect')
            flag = 1



    if flag == 0:
        messages.success(request,'Password has been changed succesfully')

        
    

    return render(request,'change-password.html',context = {'id':id,'type':type,'flag':flag})

@login_required
def doctor_dashboard(request,id):
    doctor_info = Doctor.objects.get(id = id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')
    
    appointments = Appointments.objects.filter(Doctor = id)
    name = Doctor.objects.get(id = id).name
    req = Request.objects.filter(Doctor = id)
    context = {'id':id,'Appointments':appointments,'Requests':req,'name':name}
    return render(request,'doctor-real.html',context = context)


@login_required
def delete_appointment_from_d(request,id,iid):
    doctor_info = Doctor.objects.get(id = id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')
    
    d = Appointments.objects.get(id = iid)
    print(d)
    d.delete()
    return redirect(f'/doctor_dashboard/{id}')
    

def appointments_doctor(request,id):
    doctor_info = Doctor.objects.get(id = id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')
    
    appointments = Appointments_request.objects.filter(Doctor = id)
    name = Doctor.objects.get(id = id).name
    req = Request.objects.filter(Doctor = id)
    context = {'id':id,'Appointments':appointments,'Requests':req,'name':name}
    return render(request,'doctor-appointments.html',context = context)

def appointments_req(request,id,iid,status):
    if status == 'YES':
        app_req = Appointments_request.objects.get(id = iid)
        d = Appointments.objects.create(
            patient_name = app_req.patient_name,
            gender = app_req.gender,
            Appointment_date = app_req.Appointment_date,
            age = app_req.age,
            reason = app_req.reason,
            Doctor = app_req.Doctor
            )
        d.save()
        app_req.delete()

        return redirect(f'/appointments/{id}')
    else:
        app_req = Appointments_request.objects.get(id = iid)
        app_req.delete()
        return redirect(f'/appointments/{id}')

@login_required
def organ_search(request,id):
    
    flag = 0
    doctor_info = Doctor.objects.get(id = id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')
    
    d = Doctor.objects.get(id = id)
    o = Organ.objects.filter(hospital = d.hospital)
    context = {'organ_info':o}
    patient_info = Patient.objects.filter(doctor = id)
    context = {'id':id, 'organ_info':o,'patient_info':patient_info,'flag':flag}
    print(o)
    


    if request.method == "POST":
        organ_name = request.POST.get('organ_name')
        blood_group = request.POST.get('blood_group')
        patient_id = request.POST.get('patient_name')
        if patient_id  == "":
            messages.error(request,"Patient not selected")
            return redirect(f'/doctor_organ_search/{id}')

    

        

        
        

        if organ_name == "" or blood_group == "":
            messages.error(request,"Enter all Fields")
            return redirect(f'/doctor_organ_search/{id}')
        else:
            o = Organ.objects.filter(hospital = d.hospital,organ_name = organ_name,blood_group = blood_group)
            flag = 1
        context = {'id':id,'organ_info':o,'patient_info':patient_info,'patient_id':patient_id,'flag':flag}
    
       
    


        
    return render(request,'doctor-organ-search.html',context = context)

@login_required
def doctor_request(request, doctor_id, patient_id, organ_id):
    
    doctor = get_object_or_404(Doctor, id=doctor_id)
    patient = get_object_or_404(Patient, id=patient_id)
    organ = get_object_or_404(Organ, id=organ_id)
    doctor_info = Doctor.objects.get(id = doctor_id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')

   
    if Request.objects.filter(patient_name=patient.patient_name, organ=organ, Doctor=doctor).exists():
        return redirect(f'/doctor_organ_search/{doctor_id}')

   
    Request.objects.create(
        patient_name=patient.patient_name,
        organ=organ,
        status="Pending",
        Doctor=doctor
    )

    return redirect(f'/doctor_organ_search/{doctor_id}')


@login_required
def patient_management(request,doctor_id):
    p = Patient.objects.filter(doctor = doctor_id)
    if request.method == "POST":
        p = Patient.objects.filter(patient_name = request.POST.get('patient_name'))

    doctor_info = Doctor.objects.get(id = doctor_id)

    if not request.user.username == doctor_info.doctor_email:
           messages.error(request, "You do not have permission to access this dashboard.")
           return redirect('/login')

    

    context = {'doctor_id':doctor_id,'patient_info':p}
    return render(request,'doctor-patients.html',context=context)

@login_required
def hospital_organ_req(request,id):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    
    d_id =  Doctor.objects.filter(hospital = id)
    organ_info = Request.objects.filter(Doctor__in = d_id,status = "Pending")
    context = {'id':id,'organ_info':organ_info}



    return render(request,'hospital-organ-req.html',context = context)


@login_required
def action(request,action,id,iid):
    hospital_info = Hospital.objects.get(id = id)

    if not request.user.username == hospital_info.hospital_email:
        messages.error(request, "You do not have permission to access this dashboard.")
        return redirect('/login')
    
    org = Request.objects.get(id = iid)
    org.status = action
    org.save()
    

    return redirect(f'/hospital_organ_req/{id}')

def appointments_req_2(request):

    if request.method == "POST":
        name = request.POST.get('FullName')
        age = request.POST.get('Age')
        gender = request.POST.get('Gender')
        rov = request.POST.get('ReasonforVisit')
        doctor = request.POST.get('DoctorName')
        date = request.POST.get('Date')
        if not Doctor.objects.filter(name = doctor).exists():
            print("it didnt work now did it")
            messages.error(request,'Sorry invalid Doctor name')
            return redirect('/appointment_req')

        Appointments_request.objects.create(
            patient_name = name,
            Appointment_date = date,
            gender = gender,
            age = age,
            reason = rov,
            Doctor = Doctor.objects.get(name = doctor)
            )
        

    return render(request,"appointment.html")


def pledge(request):
    if request.method == 'POST':
        full_name = request.POST.get('name')
        address = request.POST.get('address')
        pin_code = request.POST.get('pincode')
        phone_number = request.POST.get('phone_no')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('dob')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        selected_organs = request.POST.getlist('organs') 
        donor = Donor(
            full_name=full_name,
            address=address,
            pin_code=pin_code,
            phone_number=phone_number,
            email=email,
            date_of_birth=date_of_birth,
            age=age,
            gender=gender,
            organs=selected_organs  
        )
        donor.save()
        
        return redirect('/pledge')  

    return render(request, 'pledge.html')

def reddirect(request):
    return redirect('/home')

@login_required
def patient_add(request,id,type):
    hospital_info = Hospital.objects.all()

    if type == "Hospital":
    
        if not request.user.username == hospital_info.get(id = id).hospital_email:
           messages.error(request,"You do not have permission to access this dashboard")
           redirect('/login')

        if request.method == "POST":
            patient_name = request.POST.get('patient_name')
            patient_age = request.POST.get('patient_age')
            patient_gender = request.POST.get('patient_gender')
            doctor = request.POST.get('doctor')
            
            if not  Doctor.objects.filter(name = doctor).exists():
                messages.error(request,'Please Enter A Valid Doctor Name')
                return redirect(f'/patient_add/{type}/{int}')

            Patient.objects.create(
                patient_name = patient_name,
                patient_age = patient_age,
                patient_gender = patient_gender,
                doctor = Doctor.objects.get(name = doctor),
                hospital = Hospital.objects.get(id = id),
            )

            return redirect(f'/hospital_dashboard/{id}')
        
        return render(request,'patient_add.html',context = {'id':id})
    

def organ_add(request,id):
    hospital_info = Hospital.objects.all()


    
    if not request.user.username == hospital_info.get(id = id).hospital_email:
           messages.error(request,"You do not have permission to access this dashboard")
           return redirect('/login')



    if request.method == "POST":
            organ_name = request.POST.get('organ_name')
            donor_name = request.POST.get('donor_name')
            donor_age = request.POST.get('donor_age')
            blood_group = request.POST.get('blood_group')
            
        

            Organ.objects.create(
                organ_name = organ_name,
                donor_age = donor_age,
                donor_name = donor_name,
                blood_group = blood_group,
                hospital = Hospital.objects.get(id = id),
            )

            return redirect(f'/hospital_dashboard/{id}')
    return render(request,'organ_add.html')
        






    
    



    


    
















