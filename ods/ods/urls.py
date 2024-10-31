"""
URL configuration for ods project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    path('appointments_req/<int:id>/<int:iid>/<str:status>',views.appointments_req,name = "appointments_req")
    
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT 
                          
                          )

urlpatterns += staticfiles_urlpatterns()