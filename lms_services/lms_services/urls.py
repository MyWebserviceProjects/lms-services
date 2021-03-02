"""lms_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from rest_framework import routers
from lms_services.restapp import views
from django.conf.urls import url
router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
#from rest_framework.authtoken.views import obtain_auth_token # add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('core/',include('core_app.urls')),
    path('api/',include('lms_services.restapp.urls')),

    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('', RedirectView.as_view(url='core/', permanent=True)),
    path('accounts/',include('django.contrib.auth.urls')),
    path('api/core/', include('rest_framework.urls')),
    #url(r'^get-token/', obtain_auth_token), # Add this line
]
