from django import forms
from .models import Student,Faculty
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        widgets = {
        'password': forms.PasswordInput(),
    }
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        widgets = {
        'password': forms.PasswordInput(),
    }
