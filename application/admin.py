from django.contrib import admin

# Register your models here.
from .models import User
@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display=['id']
    
from .models import Donor, Patient, BloodInventory, BloodRequest,organ_request

admin.site.register(Donor)

admin.site.register( Patient)

admin.site.register( BloodInventory)

admin.site.register(BloodRequest )

admin.site.register(organ_request)

