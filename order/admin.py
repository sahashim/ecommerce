from django.contrib import admin

from .models import *

admin.site.register([OrderItem, Order, Status, Coupon])
# Registering model to admin panel
