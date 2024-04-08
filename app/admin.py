from django.contrib import admin

# Register your models here.

from app.models import *



admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Employee)
admin.site.register(TaskGroup)
admin.site.register(GroupMember)
admin.site.register(Project)
admin.site.register(Tasks)
# admin.site.register(TaskAssignToGroup)
admin.site.register(TaskAssignToEmployee)
admin.site.register(Date)
admin.site.register(ActivitySheet)
admin.site.register(Billing)


admin.site.register(Datetime)
# admin.site.register(ReportingTo)
