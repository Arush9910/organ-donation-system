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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = "home"),
    path('login',views.log_in,name = "log_in"),
    path('signupd',views.signupd,name = "signupd"),
    path('pledge',views.pledge,name = "pledge"),
    path('hospital_dashboard/<int:id>',views.hospital_dashboard,name = "hospital_dashboard"),
    path('hospital_doctors/<int:id>',views.hospital_doctors,name = "hospital_doctors"),
    path('hospital_organs/<int:id>',views.hospital_organs,name = "hospital_organs"),
    path('hospital_patients/<int:id>',views.hospital_patients,name = "hospital_patients"),
    path('remove/<int:id>/<str:email>',views.remove_doctor_from_doctor,name="remove_doctor_from_doctor"),
    
    
    
]
