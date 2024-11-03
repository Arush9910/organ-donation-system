
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home,name = "home"),
    path('login',views.log_in,name = "log_in"),
    path('signupd',views.signupd,name = "signupd"),
    path('pledge',views.pledge,name = "pledge"),
    path('hospital_dashboard/<int:id>',views.hospital_dashboard,name = "hospital_dashboard"),
    path('hospital_doctors/<int:id>',views.hospital_doctors,name = "hospital_doctors"),
    path('hospital_organs/<int:id>',views.hospital_organs,name = "hospital_organs"),
    path('hospital_patients/<int:id>',views.hospital_patients,name = "hospital_patients"),
    path('remove/<int:id>/<str:email>',views.remove_doctor_from_hospital,name="remove_doctor_from_hospital"),
    path('rorgan/<int:id>/<int:organ_id>',views.remove_organ_from_hospital,name="remove_organ_from_hospital"),
    path('contact',views.contact,name = "contact"),
    path('about',views.about,name = "about"),
    path('profile/<str:type>/<int:id>',views.profile,name = "profile"),
    path('profile_edit/<str:type>/<int:id>',views.profile_edit,name = "profile_edit"),
    path('profile_passchange/<str:type>/<int:id>',views.profile_change,name = "profile_change"),
    path('doctor_dashboard/<int:id>',views.doctor_dashboard,name = "doctor_dashboard"),
    path('delete_appointment/<int:id>/<int:iid>',views.delete_appointment_from_d,name = 'delete_appointment_from_d'),
    path('appointments/<int:id>',views.appointments_doctor,name = "appointments"),
    path('appointments_req/<int:id>/<int:iid>/<str:status>',views.appointments_req,name = "appointments_req"),
    path('doctor_organ_search/<int:id>',views.organ_search,name = "organ_search"),
    path('doctor_request/<int:doctor_id>/<int:patient_id>/<int:organ_id>',views.doctor_request,name = "doctor_req"),
    path('doctor_patient_management/<int:doctor_id>',views.patient_management,name = "patient_management"),
    path('hospital_organ_req/<int:id>',views.hospital_organ_req,name = "hospital_organ_req"),
    path('hospital_organ_req/status/<int:id>/<str:action>/<int:iid>',views.action,name = "action"),
    path('appointment_req',views.appointments_req_2,name = "appointment_req"),
    path('pledge',views.pledge,name = "pledge"),
    path('',views.reddirect,name = ""),
    path('patient_add/<str:type>/<int:id>',views.patient_add,name = "patient_add"),
    path('organ_add/<int:id>',views.organ_add,name = "organ_add")

    
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT 
                          
                          )

urlpatterns += staticfiles_urlpatterns()