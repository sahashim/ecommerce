"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.urls import path, include

# The urls of the main app.
from landing.views import Custom404

urlpatterns = [
    path('secured-real-admin-page/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls')),
    path('api-auth/', include('rest_framework.urls')),
    #path('api/account/', include('account.urls')),
    #path('admin/', admin.site.urls),
    path('', include('landing.urls')),
    path('order/', include('order.urls')),
    path('product/', include('product.urls')),
    path('customer/', include('customer.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = Custom404.as_view()
# Handling 404 error
