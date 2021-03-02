from django.shortcuts import render

# Create your views here.
from django.http import Http404,HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework import viewsets,status,permissions,mixins,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView


from .permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User, Group
from .models import Student,Faculty,Category,Course,Course_Session,Enrolled_Session
from .serializers import UserSerializer,GroupSerializer,StudentSerializer,FacultySerializer,CategorySerializer,CourseSerializer,CourseSessionSerializer,EnrolledSessionSerializer
class GroupList(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
#**********************************************   
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#**********************************************
class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
#**********************************************
class FacultyList(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    
class FacultyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
#**********************************************
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#**********************************************

class CourseList(generics.ListCreateAPIView):
    #queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
        This view should return a list of all the feedbacks for
        the user as determined by the username portion of the URL.
        """
        queryset = Course.objects.all()
        exp_credit = self.request.query_params.get('credit', None)
        if exp_credit is not None:
            queryset = queryset.filter(credit=exp_credit)
        exp_categoryid = self.request.query_params.get('categoryid', None)
        if exp_categoryid is not None:
            queryset = queryset.filter(category=exp_categoryid)
        
        return queryset
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)
    
class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#**********************************************


class MyCourseSessionList(generics.ListCreateAPIView):
    #queryset = Course_Session.objects.all()
    serializer_class = CourseSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
            This view should return a list of all the payments for the currently authenticated user.
        """
        user = self.request.user
        queryset= Course_Session.objects.filter(owner=user)
        exp_courseid = self.request.query_params.get('courseid', None)
        if exp_courseid is not None:
            queryset = queryset.filter(course=exp_courseid)
        return queryset
class CourseSessionFilterList(generics.ListCreateAPIView):
    #queryset = Course_Session.objects.all()
    serializer_class = CourseSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
            This view should return a list of all the payments for the currently authenticated user.
        """
        queryset= Course_Session.objects.all()
        exp_sessionid = self.request.query_params.get('id', None)
        exp_courseid = self.request.query_params.get('courseid', None)
        exp_takenby = self.request.query_params.get('takenby', None)
        exp_rem_seats = self.request.query_params.get('remseats', None)
        if exp_sessionid is not None:
            queryset = queryset.filter(id=exp_sessionid)
        if exp_courseid is not None:
            queryset = queryset.filter(course=exp_courseid)
        if exp_takenby is not None:
            queryset = queryset.filter(taken_by=exp_takenby)
        if exp_rem_seats is not None:
            queryset = queryset.filter(rem_seats=exp_rem_seats)
        return queryset

    
class CourseSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course_Session.objects.all()
    serializer_class = CourseSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#**********************************************


class EnrolledSessionList(generics.ListCreateAPIView):
    #queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
            This view should return a list of all the payments for the currently authenticated user.
        """
        user = self.request.user
        return Enrolled_Session.objects.filter(owner=user)

class EnrolledSessionFilterList(generics.ListCreateAPIView):
    #queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    def perform_create(self, serializer):
         serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
            This view should return a list of all the payments for the currently authenticated user.
        """
        queryset= Enrolled_Session.objects.all()
        exp_id = self.request.query_params.get('id', None)
        exp_sessionid = self.request.query_params.get('sessionid', None)
        exp_enrolledby = self.request.query_params.get('enrolledby', None)
        if exp_id is not None:
            queryset = queryset.filter(id=exp_id)
        if exp_sessionid is not None:
            queryset = queryset.filter(course=exp_sessionid)
        if exp_enrolledby is not None:
            queryset = queryset.filter(enrolled_by=exp_enrolledby)
        return queryset
    
class EnrolledSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#**********************************************  

