from django.urls import path,include

from app.views import *

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r'all_tasks', AllTasks,basename='AllTasks')




urlpatterns = [
    path('',include(router.urls)),
         


    path('DisplayDepartments/',DisplayDepartments.as_view(),name='DisplayDepartments'),
    path('EmployeeRegistration/',EmployeeRegistration.as_view(),name='EmployeeRegistration'),
    path('EmployeeLogin/',EmployeeLogin.as_view(),name='EmployeeLogin'),
    path('ParticularUserTaskss/',ParticularUserTaskss.as_view(),name='ParticularUserTasks'),
    # path('ParticularUserTaskGroup/',ParticularUserTaskGroup.as_view(),name='ParticularUserTaskGroup'),
    path('EmployeeDetailsL/',EmployeeDetailsL.as_view(),name='EmployeeDetailsL'),
    path('AssignTask/',AssignTask.as_view(),name='AssignTask'),
    path('SubTaskList/<id>/',SubTaskList.as_view(),name='SubTaskList'),
    path('PendingSubTasks/',PendingSubTasks.as_view(),name='PendingSubTasks'),
    path('CompletedSubTasks/',CompletedSubTasks.as_view(),name='CompletedSubTasks'),
    path('CompletedOnTime/',CompletedOnTime.as_view(),name='CompletedOnTime'),
    path('OverDueTasks/',OverDueTasks.as_view(),name='OverDueTasks'),    
    path('UpdateRemarks/',UpdateRemarks.as_view(),name='UpdateRemarks'),
    path('CreateTasks/',CreateTasks.as_view(),name='CreateTaks'),
    path('SuperUser/',SuperUser.as_view(),name='SuperUser'),
    path('ParticularEmployeeTasks/<email>/',ParticularEmployeeTasks.as_view(),name='ParticularEmployeeTasks'),
    path('DASView/',DASView.as_view(),name='DASView'),
    path('dasview/<date>/',dasview.as_view(),name='dasview'),
    path('PendingProjects/<statuss>/',PendingProjects.as_view(),name='PendingProjects'),
    path('DisplayTaskFromDatetoDate/',DisplayTaskFromDatetoDate.as_view(),name='DisplayTaskFromDatetoDate'),
    path('AdminEmployees/',AdminEmployees.as_view(),name='AdminEmployees'),
    path('EmployeeLogout/',EmployeeLogout.as_view(),name='EmployeeLogout'),
    path('ProjectCreate/',ProjectCreate.as_view(),name='ProjectCreate'),
    path('DisplayProjects/<status>/',DisplayProjects.as_view(),name='DisplayProjects'),
    path('DisplayParticularUserTasks/<id>/',DisplayParticularUserTasks.as_view(),name='DisplayParticularUserTasks'),
    path('ProjectAssign/',ProjectAssign.as_view(),name='ProjectAssign'),
    path('BillingView/',BillingView.as_view(),name='BillingView'),
    
    path('DisplayEmployeeProjects/<employee_id>/',DisplayEmployeeProjects.as_view(),name='DisplayEmployeeProjects'),

    
    path('ReportingEmployees/<employee_id>/',ReportingEmployees.as_view(),name='ReportingEmployees'),
    path('ChangePassword/',ChangePassword.as_view(),name='ChangePassword'),

    path('ForgetPassword/<email>/',ForgetPassword.as_view(),name='ForgetPassword'),


    

]
