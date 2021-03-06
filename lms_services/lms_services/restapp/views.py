from django.shortcuts import render

# Create your views here.
from django.http import Http404,HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from rest_framework import viewsets,status,permissions,mixins,generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView


from .permissions import IsOwnerOrReadOnly,IsOwnerOnly,IsAdminOrReadOnly,IsAdminOnly,IsFacultyAdminOrReadOnly,IsFacultyOrReadOnly,IsFacultyOnly,IsStudentOnly,IsStudentOrReadOnly

from django.contrib.auth.models import User, Group
from .models import Student,Faculty,Category,Course,Course_Session,Enrolled_Session
from .serializers import UserSerializer,GroupSerializer,StudentSerializer,FacultySerializer
from .serializers import CourseSessionSerializerForView,CategorySerializer,CourseSerializer,CourseSessionSerializer,EnrolledSessionSerializer,EnrolledSessionSerializerForView
from django.http import HttpResponse

class HttpResponseNoContent(HttpResponse):
    status_code = 204
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#**********************************************
class FacultyList(generics.ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class FacultyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#**********************************************
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def list(self, request):
        queryset = self.get_queryset()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
   


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#**********************************************


class MyCourseSessionList(generics.ListAPIView):
    #queryset = Course_Session.objects.all()
    serializer_class = CourseSessionSerializerForView
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

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
class MyCourseSessionDetails(generics.RetrieveUpdateDestroyAPIView):
     queryset = Course_Session.objects.all()
     def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSessionSerializerForView
            #return EnrolledSessionSerializer
        else:
            return CourseSessionSerializer
     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CourseSessionFilterList(generics.ListCreateAPIView):
    #queryset = Course_Session.objects.all()
    serializer_class = CourseSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSessionSerializerForView
            #return EnrolledSessionSerializer
        if self.request.method == 'POST':
            return CourseSessionSerializer
    def perform_create(self, serializer):
     serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
		This view should return a list of all the payments for the currently authenticated user.
	"""
        queryset= Course_Session.objects.all()
    
        exp_courseid = self.request.query_params.get('courseid', None)
        exp_takenby = self.request.query_params.get('takenby', None)
        exp_rem_seats = self.request.query_params.get('remseats', None)
        if exp_courseid is not None:
            queryset = queryset.filter(course=exp_courseid)
        if exp_takenby is not None:
            queryset = queryset.filter(taken_by=exp_takenby)
        if exp_rem_seats is not None:
            queryset = queryset.filter(rem_seats=exp_rem_seats)
        return queryset

    
class CourseSessionDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Course_Session.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CourseSessionSerializerForView
            #return EnrolledSessionSerializer
        else:
            return CourseSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#**********************************************


class EnrolledSession(generics.ListCreateAPIView):
    #queryset = Enrolled_Session.objects.all()
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EnrolledSessionSerializerForView
            #return EnrolledSessionSerializer
        if self.request.method == 'POST':
            return EnrolledSessionSerializer
    def perform_create(self, serializer):
     serializer_class = EnrolledSessionSerializer
     serializer.save(owner=self.request.user)
    def get_queryset(self):
        """
        This view should return a list of all the payments for the currently authenticated user.
        """

        serializer_class = EnrolledSessionSerializer
        queryset= Enrolled_Session.objects.all()
     
        exp_sessionid = self.request.query_params.get('sessionid', None)
        exp_enrolledby = self.request.query_params.get('enrolledby', None)
        exp_course = self.request.query_params.get('courseid', None)
        exp_category = self.request.query_params.get('categoryid', None)
        exp_credit = self.request.query_params.get('credit', None)
        exp_takenby = self.request.query_params.get('takenby', None)
        if exp_sessionid is not None:
            queryset = queryset.filter(course=exp_sessionid)
        if exp_enrolledby is not None:
            queryset = queryset.filter(enrolled_by=exp_enrolledby)
        if exp_course is not None:
            queryset = queryset.filter(course__course=exp_course)
        if exp_category is not None:
            queryset = queryset.filter(course__course__category=exp_category)
        if exp_credit is not None:
            queryset = queryset.filter(course__course__credit=exp_credit)
        if exp_takenby is not None:
            queryset = queryset.filter(course__taken_by=exp_takenby)
        return queryset
class EnrolledSessionDetail(generics.RetrieveDestroyAPIView):
    queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MyEnrolledSessionList(generics.ListAPIView):
    #queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializerForView
    #serializer_class = EnrolledSessionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
  
    def get_queryset(self):
        """
        This view should return a list of all the payments for the currently authenticated user.
        """
        user = self.request.user
        queryset= Enrolled_Session.objects.filter(owner=user)
        exp_sessionid = self.request.query_params.get('sessionid', None)
        
        exp_course = self.request.query_params.get('courseid', None)
        exp_category = self.request.query_params.get('categoryid', None)
        exp_credit = self.request.query_params.get('credit', None)
        exp_takenby = self.request.query_params.get('takenby', None)
        if exp_sessionid is not None:
            queryset = queryset.filter(course=exp_sessionid)
        if exp_course is not None:
            queryset = queryset.filter(course__course=exp_course)
        if exp_category is not None:
            queryset = queryset.filter(course__course__category=exp_category)
        if exp_credit is not None:
            queryset = queryset.filter(course__course__credit=exp_credit)
        if exp_takenby is not None:
            queryset = queryset.filter(course__taken_by=exp_takenby)
        return queryset

class MyEnrolledSessionDetail(generics.RetrieveDestroyAPIView):
    queryset = Enrolled_Session.objects.all()
    serializer_class = EnrolledSessionSerializerForView
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#**********************************************  

