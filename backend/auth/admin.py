from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'Location', 'PhoneNo' ]
    
