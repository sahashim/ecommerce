from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

# The urls of customer app.
urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='customer_signup'),
    path('login/', CustomerLoginView.as_view(), name='customer_login'),
    path('logout/', LogoutView.as_view(), name='customer_logout'),
    path('panel/', PanelView.as_view(), name='panel'),
    path('panel/history/', OrderView.as_view(), name='history_order'),
    # path('panel/address/', AddressView.as_view(), name='address_list'),
    # path('panel/address/delete/<int:pk>', DeleteAddressesView.as_view(), name='delete_address'),
    # path('panel/address/add/', AddAddressesView.as_view(), name='add_address'),
    path('panel/profile', ProfileView.as_view(), name='profile_view'),
    path('panel/profile/update/<int:pk>', UpdateProfileView.as_view(), name='update_profile'),
    path('panel/profile/password/', PasswordChange.as_view(), name='password'),
]

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='address')
urlpatterns += router.urls