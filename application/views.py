from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donor, Patient, BloodInventory, BloodRequest,blood,match_donoation,organ_request
from .models import User
from django.contrib.auth import login,logout,authenticate
# Home View
def home(request):
    return render(request, 'home.html')
def register(request):
    if request.method == 'POST':
        first_name = request.POST['name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmation_password = request.POST['cnfm_password']
        role = request.POST['role']  # Fetch role correctly
        print("Role selected:", role)
        if password == confirmation_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists, please choose a different one.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists, please choose a different one.')
                return redirect('register')
            else:
                # Create the user (without 'role' as User model doesn't have it)
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    role=role,
                )
                user.save()
                if role == 'patient':
                    blood_types = blood.objects.all()
                    userinfo = User.objects.filter(role=role).order_by('-id')  # Fetch latest users
                    return render(request, "patient.html", {"blood_types": blood_types, 'userinfo': userinfo})
                elif role == 'donor':
                    userinfo = User.objects.filter(role=role).order_by('-id') 
                    blood_types = blood.objects.all()
                    return render(request, 'donor.html', {"blood_types": blood_types, 'users': userinfo})
                else:
                    messages.success(request, f'Successfully added new user: {username}')
                    return redirect('register')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'please check the password...')
            return redirect('login_patient')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def add_patient(request):
    blood_types = blood.objects.all()
    userinfo=User.objects.filter(role='patient').order_by('-id')
    if request.method == "POST":
        person = request.POST.get('id')
        date_of_birth = request.POST.get("date_of_birth")
        gender = request.POST.get("gender")
        blood_type_id = request.POST.get("blood_type")
        chronic_conditions = request.POST.get("chronic_conditions")
        medications = request.POST.get("medications")
        emergency_contact = request.POST.get("emergency_contact")
        last_checkup_date = request.POST.get("last_checkup_date")
        required=request.POST['required']
        blood_type = blood.objects.get(id=blood_type_id) 
        p=User.objects.get(id=person)
        patient, created = Patient.objects.update_or_create(
            user=p,
            defaults={
                "date_of_birth": date_of_birth,
                "gender": gender,
                "blood_type": blood_type,
                "chronic_conditions": chronic_conditions,
                "medications": medications,
                "emergency_contact": emergency_contact,
                "last_checkup_date": last_checkup_date,
                "required":required,
            }
        )
        print(required)
        patient = Patient.objects.filter(required=required).order_by('-id')  
        blood_types = blood.objects.all()
        if required == 'Blood':  
            return render(request, "bloodrequest.html", {"blood_types": blood_types,'patient':patient})
        else:
            return render(request,'organrequest.html', {"blood_types": blood_types,'patients':patient})
    return render(request, "patient.html", {"blood_types": blood_types,'userinfo':userinfo})
from django.shortcuts import render, redirect
from .models import Donor, User,blood

def add_donor(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        category= request.POST.get('category')
        blood_type_id = request.POST.get('blood_type')
        organ = request.POST.get('organ', '')
        last_donation = request.POST.get('last_donation')
        userinfo = User.objects.get(id=user_id)
        blood_type_obj = blood.objects.get(id=blood_type_id)
        Donor.objects.create(
            user=userinfo,
            category=category,
            blood_type=blood_type_obj,
            organ=organ,
            last_donation=last_donation if last_donation else None,
        )
        return redirect('donor_info') 
    users = User.objects.filter(role='donor').order_by('-id')
    blood_types = blood.objects.all()
    return render(request, 'donor.html', {
        'users': users,
        'blood_types': blood_types
    })

from django.shortcuts import render, redirect
from .models import BloodRequest, blood, Patient
from django.contrib.auth.decorators import login_required

@login_required
def blood_request(request):
    patient = Patient.objects.filter(required='Blood').order_by('-id')  
    blood_types = blood.objects.all()  
    if request.method == "POST":
        p= request.POST.get("patient")
        blood_type_id = request.POST.get("blood_type_needed")
        quantity_needed = request.POST.get("quantity_needed")
        blood_type = blood.objects.get(id=blood_type_id) 
        BloodRequest.objects.create(
            patient=Patient.objects.get(id=p),
            blood_type_needed=blood_type,
            quantity_needed=quantity_needed
        )
        return redirect('blood_request')
    return render(request, "bloodrequest.html", {"blood_types": blood_types,'patient':patient})
def patient_info(request):
    info=Patient.objects.all().order_by('-id')
    return render(request,'userinfo.html',{'patient':info})

def donor_info(request):
    info=Donor.objects.all().order_by('-id')
    return render(request,'userinfo.html',{'donor':info})

def add_blood_group(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            blood.objects.create(name=name)
            return redirect('add_blood_group')
    blood_groups = blood.objects.all()  
    return render(request, 'addblood.html', {'blood_groups': blood_groups})

def organ_request_view(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        blood_type_id = request.POST.get('blood_type')
        organ_needed = request.POST.get('organ_needed')
        # Fetch related objects
        patient = Patient.objects.get(id=patient_id)
        blood_type = blood.objects.get(id=blood_type_id)
        print(organ_needed)
        # Create organ request entry
        organ_request.objects.create(
            patient=patient,
            blood_type=blood_type,
            organ_needed=organ_needed,
        )
        return redirect('/')
    patients = Patient.objects.all()
    blood_types = blood.objects.all()
    return render(request, 'organrequest.html', {
        'patients': patients,
        'blood_types': blood_types
    })
def blood_inventory(request):
    if request.method == 'POST':
        blood_type_id = request.POST.get('blood_type')
        quantity = int(request.POST.get('quantity'))

        blood_type = blood.objects.get(id=blood_type_id)

        # Check if blood type exists in inventory
        inventory, created = BloodInventory.objects.get_or_create(
            blood_type=blood_type,
            defaults={'quantity': quantity,}
        )
        if not created:
            inventory.quantity += quantity
            inventory.save()
        return redirect('blood_inventory')  
    inventory_list = BloodInventory.objects.all()
    blood_types = blood.objects.all()
    return render(request, 'bloodinventory.html', {
        'inventory_list': inventory_list,
        'blood_types': blood_types
    })
def checkmatch(request):
    patients = Patient.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        patient = get_object_or_404(Patient, id=patient_id)

        donor_info = None
        bld = None  # Default to None if blood is not required
        if patient.required.lower() == 'blood':
            print('--')  # Blood Match
          #  bld = BloodInventory.objects.get(blood_type=patient.blood_type)
            donor_info = Donor.objects.filter(blood_type=patient.blood_type, category='Blood')
            print(donor_info)
        elif patient.required.lower() == 'organ': 
            organ_required=organ_request.objects.get(patient=patient)
            donor_info = Donor.objects.filter(organ=organ_required.organ_needed)
        return render(request, 'checkmatch.html', {
            'patients': patients,
            'donor_info': donor_info,
            'blood': bld,
            'patient': patient,
        })
    return render(request, 'checkmatch.html', {'patients': patients})
def match_view(request):
    if request.method=='POST':
        patient_id=request.POST['patient_id']
        donor_id=request.POST['donor_id']
        s=match_donoation.objects.create(patient=Patient.objects.get(id=patient_id),donor=Donor.objects.get(id=donor_id))
        s.save()
        messages.error(request,'request send')
        return redirect('checkmatch')
def request(request):
    user=request.user
    if user.role=='patient':
        patient=Patient.objects.get(user=request.user)
        mtch=match_donoation.objects.filter(patient=patient)
    else:
        donor=Donor.objects.get(user=user)
        mtch=match_donoation.objects.filter(donor=donor)
    return render(request,'history.html',{'mtch':mtch})
def accept(request,pk):
    mtch=match_donoation.objects.get(id=pk)
    mtch.status='Approved'
    mtch.save()
    return redirect('/')