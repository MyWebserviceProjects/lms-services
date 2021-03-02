from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.core.validators import MaxValueValidator, MinValueValidator

class Student(models.Model):
    name = models.CharField(max_length=70, blank=True, default='')
    #group = models.ForeignKey('auth.Group', related_name='students', null=True,on_delete=models.CASCADE)
    dob = models.DateField(blank=True,null=True,help_text='Enter you DOB')
    phone = models.CharField(max_length=10, blank=True)
    email = models.EmailField(max_length=200,blank=False, default='')
    password = models.CharField(max_length=200,blank=False, default='')
    address = models.CharField(max_length=200,blank=True, default='')
    city = models.CharField(max_length=200,blank=True, default='')
    pin = models.IntegerField(blank=True)
    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Student-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
class Faculty(models.Model):
    name = models.CharField(max_length=70, blank=True, default='')
    #group = models.ForeignKey('auth.Group', related_name='faculties', null=True,on_delete=models.CASCADE)
    dob = models.DateField(blank=True,null=True,help_text='Enter you DOB')
    phone = models.CharField(max_length=10,blank=True)
    email = models.EmailField(max_length=200,blank=False, default='')
    password = models.CharField(max_length=200,blank=False, default='')
    address = models.CharField(max_length=200,blank=True, default='')
    city = models.CharField(max_length=200,blank=True, default='')
    pin = models.IntegerField(blank=True)
    class Meta:
        ordering = ['id']
    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Faculty-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
class Category(models.Model):
    name= models.CharField(max_length=200, help_text='Enter Category Name')
    class Meta:
        ordering = ['id']
    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Category-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Course(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE, help_text='Enter Category')
    name=models.CharField(max_length=200, help_text='Enter course name')
    credit=models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)],help_text='Enter credit score')
    duration=models.IntegerField(validators=[MinValueValidator(1)],help_text='Enter course duration')
    owner = models.ForeignKey('auth.User', related_name='courses_created', null=True,on_delete=models.CASCADE)
    class Meta:
        ordering = ['category']
    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Course-detail', args=[str(self.id)])
    def __str__(self):  
        """String for representing the Model object."""
        return self.name
    
class Course_Session(models.Model):
    course=models.ForeignKey('Course',null=True,on_delete=models.CASCADE, help_text='Enter Course ')
    taken_by=models.ForeignKey('Faculty',null=True,on_delete=models.CASCADE, help_text='Enter Faculty')
    owner = models.ForeignKey('auth.User', related_name='courses_taken', null=True,on_delete=models.CASCADE)
    tot_seats=models.IntegerField(validators=[MinValueValidator(1)],null=True,help_text='Enter total seats')
    rem_seats=models.IntegerField(validators=[MinValueValidator(0)],null=True,help_text='Enter remaining seats')
    start_date=models.DateField(null=True,help_text='Enter course start date')
    end_date=models.DateField(null=True,help_text='Enter course end date')
    class Meta:
        ordering = ['course__category','start_date','course','taken_by']
    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Session-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return "Course: " + self.course.name +  "; Start date: " + str(self.start_date) +   "; End Date: " + str(self.end_date)
    @property
    def is_available(self):
        if self.rem_seats==0: #seats remaning >0
            return False
        if date.today() < self.start_date: #future start date
            return False
        if date.today() > self.start_date: #past end date
            return False        
        return True

class Enrolled_Session(models.Model):
    enrolled_by=models.ForeignKey('Student',on_delete=models.CASCADE, help_text='Enter User ')
    course=models.ForeignKey('Course_Session',on_delete=models.CASCADE, help_text='Enter Course Session ')
    owner = models.ForeignKey('auth.User', related_name='courses_enrolled', null=True,on_delete=models.CASCADE)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this customer."""
        return reverse('Enrolled-Session-detail', args=[str(self.id)])
    def __str__(self):
        """String for representing the Model object."""
        return self.course.course.name
    
