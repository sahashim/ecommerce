# Register your models here.
from django.contrib import admin

from landing.models import Location


class LocationShow(admin.ModelAdmin):
    """
    Customizing appearance of ShopLocations on admin panel.
    """
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 15


admin.site.register(Location, LocationShow)
