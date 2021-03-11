from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User,Group

import json

from .models import Student
from .serializers import StudentSerializer
from .models import Faculty
from .serializers import FacultySerializer
@api_view(['POST'])
def register(request):
        if request.method == 'POST':
                new_user_data = JSONParser().parse(request)
                user_password = new_user_data['password']
                user_email = new_user_data['email']
                user_role = new_user_data['role']
                if user_email is not None and user_role is not None:    
                        students = Student.objects.all()
                        student = students.filter(email__icontains=user_email)          
                        faculties = Faculty.objects.all()                               
                        faculty = faculties.filter(email__icontains=user_email) 
                        if(len(student) == 0 and len(faculty) == 0):
                                if (user_role == "faculty" or user_role == "student"):
                                        # TODO - password hashing
                                        serializer = None
                                        if user_role == "student":
                                                serializer = StudentSerializer(data=new_user_data)
                                                group = Group.objects.get(name='student')

                                                user = User.objects.create_user(username=user_email,
                                                                         email=user_email,
                                                                         password=user_password)
                                                group.user_set.add(user)
                                        if user_role == "faculty":
                                                # TODO - handle expertise details
                                                serializer = FacultySerializer(data=new_user_data)
                                                group = Group.objects.get(name='faculty')
                                                user = User.objects.create_user(username=user_email,
                                                                         email=user_email,
                                                                         password=user_password)
                                                group.user_set.add(user)
                                        if serializer.is_valid():
                                                serializer.save()
                                                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
                                        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                        return JsonResponse({'message': 'Role Not supported!'}, status=status.HTTP_204_NO_CONTENT)              
                        else:
                                return JsonResponse({'message': 'User already exists!'}, status=status.HTTP_204_NO_CONTENT)       
                else:
                        return JsonResponse({'message': 'Check the registration details again!'}, status=status.HTTP_204_NO_CONTENT)       
@api_view(['POST'])
def login(request):
        print("login start")
        if request.method == 'POST':
                #print(request)
                user_data = JSONParser().parse(request)
                #print(user_data)
                user_email = user_data['email']
                user_password = user_data['password']
                user_role = user_data['role']           
                print(user_email, user_password, user_role)
                if user_email is not None and user_role is not None and user_password is not None:      
                        # TODO - password hashing
                        if (user_role == "student" or user_role == "faculty"):
                                print(user_role)
                                if user_role == "student":
                                        students = Student.objects.all()
                                        student = students.filter(email__icontains=user_email)  
                                        student = student.filter(password__icontains=user_password)
                                        if(len(student)!=0):
                                                serializer = StudentSerializer(student, many=True)
                                        else:
                                                return JsonResponse({'message': 'Bad Credentails!'}, status=status.HTTP_204_NO_CONTENT)
                                if user_role == "faculty":
                                        faculties = Faculty.objects.all()                               
                                        faculty = faculties.filter(email__icontains=user_email) 
                                        faculty = faculty.filter(password__icontains=user_password)
                                        if(len(faculty)!=0):
                                                serializer = FacultySerializer(faculty, many=True)
                                        else:
                                                return JsonResponse({'message': 'Bad Credentails!'}, status=status.HTTP_204_NO_CONTENT)
                                print(serializer.data)
                                print("login success - inside")
                                return JsonResponse(serializer.data, safe=False)
                        else:
                                return JsonResponse({'message': 'Role Not supported!'}, status=status.HTTP_204_NO_CONTENT)  
                                            
                           
                else:
                        return JsonResponse({'message': 'Check the login details again!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def change_password(request):
        if request.method == 'PUT':
                user_data = JSONParser().parse(request)
                print(user_data)
                user_email = user_data['email']
                user_old_password = user_data['old_password']
                user_role = user_data['role']
                if user_email is not None and user_role is not None:
                        students = Student.objects.all()
                        student = students.filter(email__icontains=user_email)
                        student = student.filter(password__icontains=user_old_password).first()
                        faculties = Faculty.objects.all()       
                        faculty = faculties.filter(email__icontains=user_email)
                        faculty = faculty.filter(password__icontains=user_old_password).first()
                        if(student is not None or faculty is not None):
                                if (user_role == "student" or user_role == "faculty"):
                                        # TODO - password hashing
                                        # TODO - email
                                        serializer = None
                                        if user_role == "student":
                                                serializer = StudentSerializer(student, data=user_data) 
                                        if user_role == "faculty":
                                                serializer = FacultySerializer(faculty, data=user_data)                                                         
                                        if serializer.is_valid():
                                                serializer.save()
                                                return JsonResponse(serializer.data) 
                                        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                else:
                                        return JsonResponse({'message': 'Role Not supported!'}, status=status.HTTP_204_NO_CONTENT)              
                        else:
                                return JsonResponse({'message': 'User does not exists!'}, status=status.HTTP_204_NO_CONTENT)       
                else:
                        return JsonResponse({'message': 'Check the details again!'}, status=status.HTTP_204_NO_CONTENT)

