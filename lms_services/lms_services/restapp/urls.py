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
from django.conf.urls import url 
from django.urls import include
from django.views.generic import RedirectView
from lms_services.restapp import views
from lms_services.restapp import views_authentication
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('groups/', views.GroupList.as_view()),
    path('groups/<int:pk>/', views.GroupDetail.as_view()),

    path('core/students/', views.StudentList.as_view()),
    path('core/students/<int:pk>/', views.StudentDetail.as_view()),
    
    path('core/faculties/', views.FacultyList.as_view()),    
    path('core/faculties/<int:pk>/', views.FacultyDetail.as_view()),
    
    path('core/category/', views.CategoryList.as_view()),
    path('core/category/<int:pk>/', views.CategoryDetail.as_view()),

    path('core/courses/', views.CourseList.as_view()), #list view - all courses (with/without filters)
    path('core/courses/<int:pk>/', views.CourseDetail.as_view()), #details view - all courses (with/wihtout filters)
    
    path('core/mysessions/', views.MyCourseSessionList.as_view()), #list view- sessions taken by logged in faculties

    path('core/myenrolledsessions/', views.EnrolledSessionList.as_view()), #list view- enrolled sessions of logged in student
    path('core/myenrolledsessions/<int:pk>/', views.EnrolledSessionDetail.as_view()), #details view- enrolled sessions of logged in student
    
    path('authentication/registration/', views_authentication.register), #user registration
    path('authentication/login/', views_authentication.login),
    path('authentication/change_password/', views_authentication.change_password), #change password
    
    path('core/sessions/', views.CourseSessionFilterList.as_view()), #list view - all sessions (with/without filters)
    path('core/sessions/<int:pk>/', views.CourseSessionDetail.as_view()), #details view - edit by logged in user

    url(r'core/enrolledsessions', views.EnrolledSessionFilterList.as_view()), #list view - all sessions (with/without filters)
    path(r'docs/', include_docs_urls(title='LMS API')),
]
