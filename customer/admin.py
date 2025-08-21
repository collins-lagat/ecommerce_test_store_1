from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Customer


class CustomerAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Phone Number", {"fields": ("phone_number",)}),)


admin.site.register(Customer, CustomerAdmin)
