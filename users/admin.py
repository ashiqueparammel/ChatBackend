from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'is_google', 'is_company')
    list_filter = ('is_google', 'is_company', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'phone_number')



admin.site.register(User, CustomUserAdmin)