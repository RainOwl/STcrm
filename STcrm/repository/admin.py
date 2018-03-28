from django.contrib import admin
from repository import models

class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['status', 'contact']
    filter_horizontal = ['consult_courses', ]
    list_per_page = 3


# Register your models here.
admin.site.register(models.UserProfile)
admin.site.register(models.Role)
admin.site.register(models.Course)
admin.site.register(models.ClassList)
admin.site.register(models.CourseRecord)
admin.site.register(models.CustomerInfo, CustomerInfoAdmin)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Student)
admin.site.register(models.StudyRecord)
admin.site.register(models.Branch)
admin.site.register(models.Menus)
