from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models

# Create your models here.
from core.models import BaseModel
from core.validators import check_phone
from django.utils.translation import gettext_lazy as _



#status
class Status(models.TextChoices):
    USUAL = 'UA', 'usual',
    DELETED = 'DT', 'deleted'
    COMPLETE = 'CM', 'complete'
    PREMIUM = 'PR', 'premium'


class MyUserManager(BaseUserManager):

    def create_user(self, phone, password, **extra_fields):
        try:
            phone = check_phone(phone)
        except Exception as e:
            raise ValueError('phone number is not a valid phone')
        user = self.model(phone = phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    """
    The customer model.
    """

    name = models.CharField(max_length=50, default='No Name', help_text="Customer name", null=False, blank=False)
    email = models.EmailField(max_length=50, default="ex@2xample.com", null=False, help_text="Customer email",blank=True)
    phone = models.CharField(max_length=16, default="09122222222", null=False, help_text="Customer phone number",unique=True)
    password = models.CharField(max_length=32, default="111", help_text="Customer password")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    national_code = models.CharField(max_length=10, help_text="Customer national code", null=False)
    score = models.IntegerField(help_text="Customer score", default=0, null=False, blank=True, editable=False)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.USUAL)
    otp = models.CharField(max_length=6, null=True)

    REQUIRED_FIELDS = ['name','email','password','national_code']
    USERNAME_FIELD = 'phone'
    objects = MyUserManager()

    def save(self, *args, **kwargs):
        self.username = self.phone
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'



    def __str__(self):
        return f'Name: {self.name}'

    @property
    def is_complete(self):
        if self.status == 'CM':
            return True
        return False

    @property
    def is_premium(self):
        if self.status == 'PR':
            return True
        return False

    def save(self, *args, **kwargs):
        self.username = self.phone
        return super().save(*args, **kwargs)


class Address(BaseModel):
    """
    The address model
    """
    country = models.CharField(max_length=50, default='Country', help_text="Country name")
    city = models.CharField(max_length=50, default='City', help_text="City name")
    street = models.CharField(max_length=200, default='Address', help_text="Full Address")
    zipcode = models.CharField(default='1111111111', help_text="Zip Code", max_length=11, null=True, blank=True)
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT, null=True, blank=True)
    count = models.IntegerField(default=0, editable=False)

    @property
    def is_favorite(self):
        if self.count > 2:
            return True
        return False




    def __str__(self):
        return f'Address: {self.street} , {self.city} , {self.country} Postal Code: {self.zipcode}'

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
