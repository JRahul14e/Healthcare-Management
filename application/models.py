from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('donor', 'Donor'),
        ('patient', 'Patient'),
        ('staff', 'Staff'), 
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    mobile=models.DecimalField(max_digits=12, decimal_places=0,default=0)


class blood(models.Model):
    name=models.CharField(max_length=30)
    
class Donor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category=models.TextField(default='Blood')
    blood_type = models.ForeignKey(blood,on_delete=models.CASCADE)
    organ=models.CharField(max_length=30,blank=True)
    last_donation = models.DateField(null=True, blank=True)
    donated=models.BooleanField(default=False)

class Patient(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_type = models.ForeignKey(blood,on_delete=models.CASCADE)
    chronic_conditions = models.TextField(blank=True, null=True)  # E.g., Diabetes, Hypertension
    medications = models.TextField(blank=True, null=True)  # List of ongoing medications
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    required=models.CharField(max_length=15, blank=True, null=True)
    last_checkup_date = models.DateField(null=True, blank=True) 
    status=models.TextField(default='pending')

# Blood Inventory Model
class BloodInventory(models.Model):
    blood_type = models.ForeignKey(blood,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

# Blood Request Model
class BloodRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_type_needed = models.ForeignKey(blood,on_delete=models.CASCADE)
    quantity_needed = models.IntegerField()
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

class organ_request(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    blood_type= models.ForeignKey(blood,on_delete=models.CASCADE)
    organ_needed = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('denied', 'Denied')], default='pending')
    request_date = models.DateTimeField(auto_now_add=True)

class match_donoation(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    donor=models.ForeignKey(Donor,on_delete=models.CASCADE)
    status=models.TextField(default='pending')
    