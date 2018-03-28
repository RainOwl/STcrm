from repository.BaseAdmin import BaseAdmin
from repository import models
from myadmin.sites import site

class CustomerInfoAdmin(BaseAdmin):
    list_display = ['id','name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
    list_filter = ['source', 'consultant', 'status','date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['status', 'contact']
    filter_horizontal = ['consult_courses', ]
    list_per_page = 3

class UserProfileAdmin(BaseAdmin):
    list_display = ('user','name','role')

class CourseAdmin(BaseAdmin):
    list_display = ['id','name','price','period']

# Register your models here.
site.register(models.UserProfile, UserProfileAdmin)
site.register(models.Role)
site.register(models.Course, CourseAdmin)
site.register(models.ClassList)
site.register(models.CourseRecord)
site.register(models.CustomerInfo, CustomerInfoAdmin)
site.register(models.CustomerFollowUp)
site.register(models.Student)
site.register(models.StudyRecord)
site.register(models.Branch)
site.register(models.Menus)

