"""Health_care URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from application import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login',views.login_view,name="login"),
    path('login/admin/', views.login_view, name='login_admin'),
    path('login/donor/', views.login_view, name='login_donor'),
    path('login/patient/', views.login_view, name='login_patient'),
    path('login/staff/', views.login_view, name='login_staff'),
    path('logout', views.logout_view, name='logout'),
    path('add-role', views.register, name='register'),
    path("patients-info/", views.patient_info, name="patients_info"),
    path('add-patient',views.add_patient,name='add_patient'),
    path('add-donor',views.add_donor, name='add_donor'),
    path("donor-info/", views.donor_info, name="donor_info"),
    path('add-blood/',views.add_blood_group, name='add_blood_group'),
    path('blood-request',views.blood_request,name='blood_request'),
    path('organ-request',views.organ_request_view,name='organ_request'),
    path('blood-inventory/',views.blood_inventory, name='blood_inventory'),
    path('checkmatch',views.checkmatch, name='checkmatch'),
    path('match_view',views.match_view,name='match_view'),
    path('math-status',views.request,name='match_status'),
    path('accept/<int:pk>/',views.accept,name='accept')
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)