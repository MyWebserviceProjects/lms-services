from django.contrib import admin

# Register your models here.
from .models import Student,Faculty,Category,Course,Course_Session,Enrolled_Session

#admin.site.register(Role)
#admin.site.register(User)
#admin.site.register(Category)
#admin.site.register(Course)
#admin.site.register(Course_Session)
#admin.site.register(Enrolled_Session)

#class RoleAdmin(admin.ModelAdmin):
#    list_display=('id','name','comments')

class StudentAdmin(admin.ModelAdmin):
    list_display=('id','name','dob')
    fieldsets = ((None, {'fields': ('name','password','dob',  )}),
                 ('Location', {'fields': ('address', 'city','pin'   )}),
                 ('Contact', {'fields': ('email','phone')}),)
class FacultyAdmin(admin.ModelAdmin):
    list_display=('id','name','dob')
    fieldsets = ((None, {'fields': ('name','password','dob',  )}),
                 ('Location', {'fields': ('address', 'city','pin'   )}),
                 ('Contact', {'fields': ('email','phone')}),)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('id','name')
    
class CourseAdmin(admin.ModelAdmin):
    list_display=('id','category','name','credit','duration')
    list_filter = ('category', 'credit')


class Course_SessionAdmin(admin.ModelAdmin):
    list_display=('id','get_category','course', 'get_facultyname', 'get_coursecredit','tot_seats','rem_seats','start_date','end_date')
    def get_coursecredit(self, obj):
        return obj.course.credit
    get_coursecredit.short_description = 'Credit'  #Renames column head
    def get_category(self,obj):
        return obj.course.category
    get_category.short_description = 'Category'  #Renames column head

    def get_facultyname(self,obj):
        return obj.taken_by.name
    get_facultyname.short_description = 'Taken By'  #Renames column head

    list_filter = ('start_date', 'end_date','course','taken_by','course__category','course__credit')
    pass

class Enrolled_SessionAdmin(admin.ModelAdmin):
    list_display=('get_course','get_coursecategory','get_sdate','get_edate','get_userName','get_facultyname')
    list_filter = ('course__taken_by', 'enrolled_by__name','course__course__category','course__course__credit')

    def get_sdate(self,obj):
        return obj.course.start_date
    def get_edate(self,obj):
        return obj.course.end_date
    
    def get_course(self,obj):
        return obj.course.course.name
    def get_coursecategory(self,obj):
        return obj.course.course.category
    def get_userName(self,obj):
        return obj.enrolled_by.name
    def get_facultyname(self,obj):
        return obj.course.taken_by.name

    get_sdate.short_description = 'Course Start Date'  #Renames column head
    get_edate.short_description = 'Course End Date'  #Renames column head
    get_course.short_description = 'Course Name'  #Renames column head
    get_coursecategory.short_description = 'Course Category'  #Renames column head
    get_facultyname.short_description = 'Faculty Name'  #Renames column head
    get_userName.short_description = 'Student Name'  #Renames column head


    pass

#admin.site.register(Role,RoleAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(Faculty,FacultyAdmin)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Course,CourseAdmin)
admin.site.register(Course_Session,Course_SessionAdmin)
admin.site.register(Enrolled_Session,Enrolled_SessionAdmin)
