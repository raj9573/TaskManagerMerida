from django.db import models

# Create your models here.
import uuid

from django.utils import timezone

from django.contrib.auth.models import User

def generate_employee_id():
    return 'MER' + str(uuid.uuid4().hex)[:7].upper()

class Department(models.Model):

    department_name =  models.CharField(max_length=100)


    def __str__(self):
        return self.department_name
    

class Position(models.Model):

    position = models.CharField(max_length=100)

    def __str__(self):
        return self.position







class Employee(models.Model):
    STATUS_CHOICES = (
        ('employee','employee'),
        ('team_leader','team_leader'),
        ('manager','manager'),
        ('admin','admin'),
    )

    employee_id = models.CharField(max_length=100,default=generate_employee_id)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    password = models.CharField(max_length=2000000)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    registered_date = models.DateTimeField(default=timezone.now) 
    logged_in = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    status = models.CharField(max_length=100)
    reporting_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='reportees', null=True, blank=True)
    # team_leader = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='team_members', null=True, blank=True)
                         
                         
    def __str__(self):
        return self.name
    

# class ReportingTo(models.Model):
#     department =  models.ForeignKey(Department,on_delete=models.CASCADE,related_name='employees')
#     reporting_to = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='reporting_to')


    

class TaskGroup(models.Model):
    reporting_manager = models.ForeignKey(Employee,on_delete=models.CASCADE)
    group_name =  models.CharField(max_length=100)

    def __str__(self):
        return self.group_name
    
 
class GroupMember(models.Model):
    group_name = models.ForeignKey(TaskGroup,on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE)
    added_date = models.DateTimeField(default=timezone.now)

STATUS_CHOICES = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('over_due', 'Overdue'),
        ('completed_on_time', 'Completed On Time'),
        ('completed_after_time', 'Completed After Time')
    ]
class Project(models.Model):
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    created_by = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True, blank=True)
    task_name = models.CharField(max_length=100)
    priority = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    completed_date = models.DateTimeField(null=True, blank=True)
    remarks =  models.TextField(blank=True,null=True) 
    due_date = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.task_name
    
    def save(self, *args, **kwargs):
        if self.completed_date:
            if self.completed_date > self.due_date:
                self.status = 'completed_after_time'
            elif self.completed_date <= self.due_date:
                self.status = 'completed_on_time'
        else:
            if self.due_date and self.due_date < timezone.now():
                self.status = 'over_due'
            else:
                self.status = 'pending'
        super().save(*args, **kwargs)

        # all_tasks_completed = self.tasks.filter(status__in=['pending', 'in_progress']).count() == 0
        # if all_tasks_completed:
        #     self.status = 'completed'
        #     self.save(update_fields=['status'])  


class Tasks(models.Model):
    task_list = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    completed_date = models.DateTimeField(blank=True,null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=100,blank=True,null=True)
    priority = models.IntegerField()


    def __str__(self):
        return self.task_name
    

    def save(self, *args, **kwargs):
        if self.completed_date and self.completed_date > self.due_date:
            print(self.completed_date)
            self.status = 'completed_after_time'
        elif self.completed_date and self.completed_date <= self.due_date:
            self.status = 'completed_on_time'
        super(Tasks, self).save(*args, **kwargs)


# class TaskAssignToGroup(models.Model):
#     task_name = models.ForeignKey(TaskList, on_delete=models.CASCADE)
#     group_name = models.ForeignKey(TaskGroup, on_delete=models.CASCADE)
#     assigned_date = models.DateTimeField(default=timezone.now)
#     status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
#     completed_date = models.DateTimeField(null=True, blank=True)

#     def save(self, *args, **kwargs):
#         if self.completed_date and self.completed_date > self.task_name.due_date:
#             self.status = 'completed_after_time'
#         elif self.completed_date and self.completed_date <= self.task_name.due_date:
#             self.status = 'completed_on_time'
#         super(TaskAssignToGroup, self).save(*args, **kwargs)


class TaskAssignToEmployee(models.Model):
    created_by = models.ForeignKey(Employee,on_delete=models.DO_NOTHING,related_name='created_by',null=True,blank=True)
    task_name = models.ForeignKey(Project, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='assigned_to')
    created_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    completed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):

        return self.employee.name + ' ' + self.task_name.task_name

    def save(self, *args, **kwargs):
        if self.completed_date and self.completed_date > self.task_name.due_date:
            self.status = 'completed_after_time'
        elif self.completed_date and self.completed_date <= self.task_name.due_date:
            self.status = 'completed_on_time'
        super(TaskAssignToEmployee, self).save(*args, **kwargs)



class Date(models.Model):
    
    date = models.DateField(default=timezone.now)

from datetime import datetime


class ActivitySheet(models.Model):
    employee =  models.ForeignKey(Employee,on_delete=models.CASCADE)
    # date =  models.ForeignKey(Date,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    assigned_time =  models.CharField(max_length=100,default='')
    estimated_completed_time =  models.CharField(max_length=100,default='')
    action_planned = models.TextField(default='')
    action_acheived = models.CharField(max_length=100,choices=STATUS_CHOICES,default='pending')
    remarks = models.TextField(default='')
    
    
class Billing(models.Model):
    employee =  models.ForeignKey(Employee,on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    billing_projected = models.IntegerField(blank=True,default=0)
    billing_acheived =  models.IntegerField(blank=True,default=0)
    collection_projected =  models.IntegerField(blank=True,default=0)
    collection_acheived =  models.IntegerField(blank=True,default=0)


    # def save(self, *args, **kwargs):
    #     if self.action_acheived == 'pending' and self.assigned_time and self.estimated_completed_time:
    #         assigned_time = datetime.strptime(self.assigned_time, '%H:%M')
    #         estimated_completed_time = datetime.strptime(self.estimated_completed_time, '%H:%M')
    #         current_time = datetime.now().time()

    #         if current_time > estimated_completed_time.time():
    #             self.action_acheived = 'completed_after_time'
    #         elif current_time <= estimated_completed_time.time():
    #             self.action_acheived = 'completed_on_time'

    #     super().save(*args, **kwargs)
    
    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     # Get the user from the context
    #     user = self.context['request'].user
    #     # Check if the user is in the HR department
    #     if user.employee.department.department_name.lower() != 'hr department':
    #         # Remove the fields that shouldn't be visible
    #         data.pop('billing_projected', None)
    #         data.pop('billing_acheived', None)
    #         data.pop('collection_projected', None)
    #         data.pop('collection_acheived', None)
    #     return data



class Datetime(models.Model):
    completed_date = models.DateTimeField(blank=True,null=True)




class OTP(models.Model):
    employee =  models.ForeignKey(Employee,on_delete=models.CASCADE)
    otp = models.CharField(max_length=100)



