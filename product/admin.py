from django.contrib import admin

from .models import *


class CategoryShow(admin.ModelAdmin):
    """
    An admin model class for costuming categories on admin panel.
    """
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 15


class CommentShow(admin.ModelAdmin):
    """
    An admin model class for costuming comments on admin panel.
    """
    search_fields = ['content']
    list_per_page = 15


class ProductShow(admin.ModelAdmin):
    """
    An admin model class for costuming products on admin panel.
    """
    list_display = ['name', 'price']
    search_fields = ['name']
    list_per_page = 15


class DiscountShow(admin.ModelAdmin):
    """
    An admin model class for costuming discounts on admin panel.
    """
    list_display = ['description', 'amount']
    search_fields = ['description']
    list_per_page = 15


class BrandShow(admin.ModelAdmin):
    """
    An admin model class for costuming brands on admin panel.
    """
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 15


admin.site.register(Category, CategoryShow)
admin.site.register(Discount, DiscountShow)
admin.site.register(Brand, BrandShow)
admin.site.register(Comment, CommentShow)
admin.site.register(Product, ProductShow)
# Registering models to admin panel
