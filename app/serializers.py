from rest_framework import serializers 



from app.models import *

from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password,check_password


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Department
        fields = '__all__'

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields ='__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.PrimaryKeyRelatedField(queryset = Department.objects.all())
    
    position = serializers.PrimaryKeyRelatedField(queryset = Position.objects.all())
    
    class Meta:
        model =  Employee

        fields = ['name','email','password','department','position','registered_date','profile_pic','reporting_to','status']

    def create(self, validated_data):
        department =  validated_data['department']
        position =  validated_data['position']
        print(department,position)
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        print(validated_data)
        return super().create(validated_data)



class EmployeeDisplaySerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    
    position =  PositionSerializer()
    
    class Meta:
        model =  Employee

        fields = ['pk','name','email','department','position','registered_date','profile_pic','status']


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['pk','task_name','priority','created_date','due_date','status']


def format_created_at(created_at):
    # Calculate the time difference between the current time and the created_at time
    time_difference = timezone.now() - created_at

    # Convert the time difference into days, hours, and minutes
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    # Define the human-readable format based on the time difference
    if days == 0:
        if hours == 0:
            if minutes == 0:
                return "Just now"
            else:
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif days == 1:
        return "1 day ago"
    elif days < 7:
        return f"{days} days ago"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} week{'s' if weeks != 1 else ''} ago"
    elif days < 365:
        months = days // 30
        return f"{months} month{'s' if months != 1 else ''} ago"
    else:
        years = days // 365
        return f"{years} year{'s' if years != 1 else ''} ago"

class UserTaskSerializer(serializers.ModelSerializer):
    task_name =TaskListSerializer()
    employee = EmployeeDisplaySerializer()
    created_by = EmployeeDisplaySerializer()
    created_date = serializers.SerializerMethodField()


    def get_created_date(self,obj):
        return format_created_at(obj.created_date)
    class Meta:
        model =  TaskAssignToEmployee
        fields ='__all__'


class TaskGroupSerializer(serializers.ModelSerializer):
    reporting_manager = EmployeeDisplaySerializer()
    class Meta:
        model = TaskGroup
        fields = '__all__'


class GroupMemberSerializer(serializers.ModelSerializer):
    group_name = TaskGroupSerializer()
    class Meta:
        model = GroupMember
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProjectSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.name
        return None
    class Meta:
        model = Project
        fields = ['id', 'assigned_to', 'created_by', 'task_name', 'priority', 'created_date', 'status', 'completed_date', 'remarks', 'due_date']
    

    def get_assigned_to(self, obj):
        # print("assigned_method is calling")
        TAO = TaskAssignToEmployee.objects.filter(task_name=obj)
        # print("this is the serializers",TAO)
        # print(obj)
        # Retrieve the assigned employee for the project
        for i in TAO:

            if i.employee.name:
                obj.assigned_to = i.employee.name
                return obj.assigned_to
            else:
                obj.assigned_to = None
                return obj.assigned_to


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model =Project
        fields = '__all__'

class EmployeeSerializerr(serializers.ModelSerializer):
    position = PositionSerializer()
    department=DepartmentSerializer()
    class Meta:
        model =  Employee
        fields = ['name','email','department','position','registered_date','profile_pic']


class TaskAssignToEmployeeSerializer(serializers.ModelSerializer):
    task_name=ProjectSerializer()
    employee = EmployeeSerializerr()
    class Meta:
        model = TaskAssignToEmployee
        fields = '__all__'


class TaskAssignToEmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAssignToEmployee
        fields = '__all__'




class TasksSerializer(serializers.ModelSerializer):
    created_by = EmployeeDisplaySerializer()
    class Meta:
        model = Tasks
        fields = '__all__'

class DailyActivitySheetSerializer(serializers.ModelSerializer):
    employee =  EmployeeDisplaySerializer()
    class Meta:
        model = ActivitySheet
        fields = '__all__'


class DailyActivityPostSheetSerializer(serializers.ModelSerializer):
    # employee =  EmployeeDisplaySerializer()
    class Meta:
        model = ActivitySheet
        fields = '__all__'


class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'