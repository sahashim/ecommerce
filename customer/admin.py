from django.contrib import admin

from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from customer.models import Customer
from .models import *

@admin.register(Address)
class AddressShow(admin.ModelAdmin):
    """
    Customizing appearance of addresses on admin panel.
    """
    search_fields = ['street']
    ordering = ['country']
    list_per_page = 15




@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Customizing users on admin panel.
    """
    list_display = ['name','phone','email','national_code'  ]
    search_fields = ['name','phone','email','national_code' ]
    list_per_page = 15



