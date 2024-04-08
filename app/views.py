from django.shortcuts import render

# Create your views here.


from app.models import *

from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import *

from django.contrib.auth.hashers import make_password,check_password

from rest_framework import status
from rest_framework.permissions import BasePermission

from app.models import *

from rest_framework.generics import ListCreateAPIView


import json

from datetime import datetime

from django.core.mail import send_mail


#session data 

global_session_data = {"user_name":"karthik12@gmail.com"}     

#display departments and positions 
class DisplayDepartments(APIView):
    def get(self,request):

        DO = Department.objects.all()

        PO = Position.objects.all()

        Department_Serializer = DepartmentSerializer(DO,many=True)
        Position_Serializer = PositionSerializer(PO,many=True)

        Registration_data = {
            'Departments':Department_Serializer.data,
            'Positions':Position_Serializer.data,
        }
        return Response(Registration_data)
    def post(self,request):
        print(request.data)
        if request.data.get("department_name"):

            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response("Department Added suceesfull",status=200)
            else:

                return Response(serializer.errors)
        elif request.data.get("position"):
            serializer = PositionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response("Position Inserted successfull")

            else:
                return Response(serializer.errors)


class sendStatus(APIView):

    pass


#Employee Registration
class EmployeeRegistration(APIView):
    def get(self,request):
        EO = Employee.objects.all()
        serializer = EmployeeDisplaySerializer(EO,many=True,context={'request':request})
        return Response(serializer.data)
        
    def post(self, request):
        # Deserialize the incoming data
        
        # serializer = EmployeeSerializer(data={
        #     'name':request.data.get('name'),
        #     'email':request.data.get('email'),
        #     'password':request.data.get('password'),
        #     'department':request.data.get('department'),
        #     'position':request.data.get('position'),
        #     'profile_pic':request.data.get('profile_pic'),
        #     'status':request.data.get('status')
        # })
        serializer = EmployeeSerializer(data=request.data)   
        
        # Validate the data
        if serializer.is_valid():
            serializer.save()

            # Save the validated data
            # instance = serializer.save()
            # instance.profile_pic = request.data.get('profile_pic')
            # instance.save()
            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return error response if data is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Employee details
def EmployeeDetails(email):
    eo = Employee.objects.get(email=email)
    return eo

#Employee Login
class EmployeeLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')


        try:
            employee = Employee.objects.get(email=email)
        except Employee.DoesNotExist:
            return Response({'message': "Employee does not exist with this email."}, status=status.HTTP_404_NOT_FOUND)

        # Check if the provided password matches the hashed password in the database
        if check_password(password, employee.password):
            # If the passwords match, set session data or perform any necessary actions
            global_session_data['user_name'] = employee.email

            # Assuming EmployeeDetails is a function that returns employee details based on email
            employeedetails = EmployeeDetails(employee.email)
            serializer = EmployeeDisplaySerializer(employeedetails, context={'request': request})
            return Response({"message":"User Credentials Matched","id":employee.id,'status':employee.status},status=status.HTTP_200_OK)
        else:
            return Response({'message': "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)


#Authentication System
class IsAuthenticatedSession(BasePermission):

    def has_permission(self, request, view):


        if global_session_data.get('user_name'):
            return True 
        else:
            return False


class EmployeeLogout(APIView):
    permission_classes = [IsAuthenticatedSession]
    def post(self,request):

        if 'user_name' in global_session_data:
            del global_session_data['user_name']

            return Response("Logout Successfull")
        else:

            return Response("Logout Failed")


class EmployeeDetailsL(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):
        if 'user_name' in global_session_data:
            user_name = global_session_data['user_name']
            employeedetails = EmployeeDetails(user_name)

            # if TeamLeader.objects.filter(leader=employeedetails).exists() or Manager.objects.filter(TeamLeader=TeamLeader.objects.filter(leader=employeedetails).exists()).exists():
            #     if TeamLeader.objects.filter(leader=employeedetails).exists():
            #         EO = Employee.objects.filter(department=employeedetails.department)
            #         serializer =  EmployeeDisplaySerializer(EO,many=True,context = {'request':request}).data
            #         data = {
            #             'user_details': EmployeeDisplaySerializer(employeedetails,context={'request':request})
            #         }
            #         return Response(serializer)
            #     else:
            #         return Response("Manager")
            #     return Response("He is manager or Team leader")
            # else:

            serializer = EmployeeDisplaySerializer(employeedetails, context={'request': request}).data


            # if TeamLeader.objects.filter(leader=employeedetails).exists():
            #     serializer['Employee_Type'] = 'Team Leader'
            # elif Manager.objects.filter(TeamLeader=TeamLeader.objects.filter(leader=employeedetails).exists()).exists():
            #     serializer['Employee_Type'] = 'Manager'

            # else:
            #     serializer['Employee_Type'] = 'Associate'
            
            return Response(serializer)


        return Response("User Not Found")

  
class ParticularUserTaskss(APIView):
    # permission_classes = [IsAuthenticatedSession]
    def get(self,request):

        email = global_session_data.get('user_name')

        
        employee_object = Employee.objects.get(email=email)
        task_object =TaskAssignToEmployee.objects.filter(employee=employee_object,status='pending')
        task_serializer = UserTaskSerializer(task_object,many=True,context={'request':request}).data
        all_tasks =TaskAssignToEmployee.objects.filter(employee=employee_object)

        
        
        completed_task_object =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed','completed_on_time','completed_after_time'))
        completed_on_time =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed_on_time'))
        completed_after_time =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed_after_time'))


       
        completed_task_serializer = UserTaskSerializer(completed_task_object,many=True,context={'request':request}).data
        completed_on_time_serializer  = UserTaskSerializer(completed_on_time,many=True,context={'request':request}).data
        completed_after_time_serializer = UserTaskSerializer(completed_after_time,many=True,context={'request':request}).data


        tasks = {
            'all_tasks':UserTaskSerializer(all_tasks,many=True,context={'request':request}).data,
            'completed_tasks':completed_task_serializer,
            'pending_tasks':task_serializer,
            'completed_on_time':completed_on_time_serializer,
            'completed_after_time':completed_after_time_serializer,

        }
        completed_task_object_count =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed','completed_on_time','completed_after_time')).count()
        
        completed_on_time_count =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed_on_time')).count()
        completed_after_time_count =TaskAssignToEmployee.objects.filter(employee=employee_object,status__in=('completed_after_time')).count()
        task_object_count =TaskAssignToEmployee.objects.filter(employee=employee_object,status='pending').count()
        tasks['count'] =        {

            'completed_task_object':completed_task_object_count,
            'completed_on_time':completed_on_time_count,
            'completed_after_time':completed_after_time_count,
            'pending_tasks':task_object_count
        } 
        # serializer = UserTaskSerializer(task_object,many=True)
        return Response(tasks)
    def put(self,request):
        global TAO
        tid =  request.data.get('id')
        status =  request.data.get('status')
        # TO = TaskAssignToEmployee.objects.get(id=tid)
        # date_of_assigned = TO.assigned_date

        if status:  # Assuming status is a string representing boolean
            TAO = Tasks.objects.get(id=tid)
            TAO.completed_date   = timezone.now()
            TAO.save()
            

            # TAO.task_list
            if Tasks.objects.filter(task_list=TAO.task_list, status__in=['pending', 'in_progress']).count() == 0:
                project = Project.objects.get(id=TAO.task_list.id)
                project.completed_date = timezone.now()
                project.save()
                return Response("Project and Task are completed succesfully")
            else:

                project = Project.objects.get(id=TAO.task_list.id)
                project.completed_date = None
                # project.status = 'pending'
                project.save()
                return Response("updated successfully ")
            return Response("Updated Successfully", status=status.HTTP_200_OK)

        else:
            Tasks.objects.filter(id=tid).update(status='pending', completed_date=None)
            project = Project.objects.get(id=TAO.task_list.id)
            project.completed_date = None
            project.save()
            return Response("Updated to pending")
    
    


class AssignTask(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):
        # pass
        email = global_session_data.get('user_name')
        eo = Employee.objects.get(email=email)
        PO = TaskAssignToEmployee.objects.filter(employee=eo)
        # return Response("hellow")
        s = TaskAssignToEmployeeSerializer(PO,many=True,context = {'request':request})

        Pending_task_object = TaskAssignToEmployee.objects.filter(employee=eo,status='completed_after_time')

        s = TaskAssignToEmployeeSerializer(Pending_task_object,many=True,context = {'request':request})

        return Response(s.data)
        
    def post(self,request):
        
        tid = request.data.get('task_id')
        to =  Project.objects.get(id = tid)
        email = global_session_data.get('user_name')
        employee_object = Employee.objects.get(email=email)

        created_by = employee_object


        assigned_to = request.data.get('employee_id')

        EO = Employee.objects.get(id = assigned_to)

        TaskAssignToEmployee.objects.create(created_by=created_by,task_name=to,employee=EO)

        return Response("Assign Taask")

class updateEmployeeTasklist(APIView):
    permission_classes = [IsAuthenticatedSession]
    def put(self,request):
        pass


class SubTaskList(APIView):
    permission_classes = [IsAuthenticatedSession]
    
    def get(self,request,id):
        try:
            PO = Project.objects.get(pk = id)
            TO = Tasks.objects.filter(task_list=PO)
            serializer = TasksSerializer(TO,many=True,context={'request':request})
            # print(serializer)
            for i in serializer.data:
                i['project']=PO.task_name
            return Response(serializer.data)
        except Exception as e:
            return Response(e)



    
class PendingSubTasks(APIView):
    permission_classes = [IsAuthenticatedSession]
    def get(self,request):
        email = global_session_data.get('user_name')

        EO =  Employee.objects.get(email=email)
        TO = Tasks.objects.filter(created_by=EO,status='pending')
        serializer = TasksSerializer(TO,many=True,context={'request':request})        
        return Response(serializer.data)


        
class CompletedSubTasks(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):
        email = global_session_data.get('user_name')
        EO =  Employee.objects.get(email=email)
        TO = Tasks.objects.filter(created_by=EO).exclude(status='pending')
        serializer = TasksSerializer(TO,many=True,context={'request':request})        
        return Response(serializer.data)

class CompletedOnTime(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):
 
        email = global_session_data.get('user_name')
        EO =  Employee.objects.get(email=email)
        TO = Tasks.objects.filter(created_by=EO,status='completed_on_time')
        serializer = TasksSerializer(TO,many=True,context={'request':request})      

        TCAT = Tasks.objects.filter(created_by=EO,status='completed_after_time')
        TCAT_serializer = TasksSerializer(TCAT,many=True,context={'request':request}).data


        task_details ={
            'completed_on_time':serializer.data,
            'completed_after_time':TCAT_serializer
        }

        return Response(task_details)


class OverDueTasks(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):
        email = global_session_data.get('user_name')
        EO =  Employee.objects.get(email=email)
        TO = Tasks.objects.filter(created_by=EO,status='over_due')
        serializer = TasksSerializer(TO,many=True,context={'request':request})      
        return Response(serializer.data)

class UpdateRemarks(APIView):
    permission_classes = [IsAuthenticatedSession]
    def put(self,request):

        tid =  request.data.get('id')
        remarks =  request.data.get('remarks')

        TAO = Tasks.objects.get(id=tid)

        TAO.remarks = remarks

        TAO.save()
        return Response("updated successfully")

class CreateTasks(APIView):
    permission_classes = [IsAuthenticatedSession]

    def post(self,request):


        employee_task_data =  request.data
        
        task_list =  request.data.get('task_list')
        task_name = request.data.get('task_name')
        due_date_str =  request.data.get('due_date')
     
        remarks =  request.data.get('remarks')
        priority =  request.data.get('priority')
        current_datetime = datetime.now()
        # due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        due_date = timezone.make_aware(datetime.strptime(due_date_str, '%Y-%m-%d'))            
                    
        # Combining due_date with current time to create a datetime object
        # due_datetime = datetime.combine(due_date, current_datetime.time())
        email = global_session_data.get('user_name')
        EO =  Employee.objects.get(email=email)
        PO = Project.objects.get(id=task_list)
        try:
        
            Tasks.objects.create(task_list=PO,created_by=EO,task_name=task_name,priority=priority,remarks=remarks,due_date=due_date)
        
        except Exception as e:
             
            return Response(e)


        return Response("data sended")



class SuperUser(APIView):
    permission_classes = [IsAuthenticatedSession]

    def get(self,request):


        EO = Employee.objects.all()
        serializer = EmployeeDisplaySerializer(EO,many=True,context={'request':request})
        return Response(serializer.data)

#-----------------------------Particular Employee Task------------------------


class ParticularEmployeeTasks(APIView):
    permission_classes = [IsAuthenticatedSession]
    def get(self,request,email):

        EO =  Employee.objects.get(email=email)
        tasks = TaskAssignToEmployee.objects.filter(employee=EO)

        serializer = UserTaskSerializer(tasks,context={'request':request},many=True)
        return Response(serializer.data)
         

#------------------------------DAS---------------------------

def DayTask(date,email,request):
    
    queryset = ActivitySheet.objects.filter(employee=Employee.objects.get(email=email),date=date)
    
    serializer = DailyActivitySheetSerializer(queryset,many=True,context={'request':request}) 
    
    return serializer


class dasview(APIView):
    permission_classes = [IsAuthenticatedSession]
    def post(self,request,date):
        email = global_session_data['user_name']
        # queryset = ActivitySheet.objects.filter(employee=Employee.objects.get(email=email),date=timezone.now().date())
        # serializer = DailyActivitySheetSerializer(queryset,many=True,context={'request':request}) 
        # return Response(serializer.data)
        result =  DayTask(date,email,request).data

        return Response(result)

class DASView(APIView):
    permission_classes = [IsAuthenticatedSession]
    def get(self,request):
        email = global_session_data['user_name']
        date = request.data.get('date')

        if date:
            # queryset = ActivitySheet.objects.filter(employee=Employee.objects.get(email=email),date=timezone.now().date())
            # serializer = DailyActivitySheetSerializer(queryset,many=True,context={'request':request}) 
            # return Response(serializer.data)
            result =  DayTask(date,email,request).data

            return Response(result)
        else:
            result = DayTask(timezone.now().date(),email,request).data
            return Response(result)
            

        # queryset = ActivitySheet.objects.filter(employee=Employee.objects.get(email=email),date=timezone.now().date())
        # serializer = DailyActivitySheetSerializer(queryset,many=True,context={'request':request}) 

        # return Response(serializer.data)
    def post(self,request):
        print(request.data)
        try:
            ied = request.data.get('id')
            email = global_session_data['user_name']

            EO = Employee.objects.get(email= email)
            request.data['employee']=EO.pk
            s = DailyActivityPostSheetSerializer(data=request.data)


            if s.is_valid():

                s.save()

                return Response("data")
            
            else:
                print(s.errors)
            
                return Response(s.errors,status=400)
        except Exception as e:
            print(e)
            return Response(e)
    def patch(self,request):
    
        email =  global_session_data['user_name']
        EO = Employee.objects.get(email=email)

        did = request.data.get('id')
        DASO =  ActivitySheet.objects.get(id=did)
        s = DailyActivityPostSheetSerializer(DASO,data=request.data,partial=True)
        if s.is_valid():
            s.save()
            return Response("data updated successfully",status=201)
        else:
            return Response(s.errors,status=400)

from django.utils import timezone
from django.db.models import Q
class BillingView(APIView):
    def put(self, request):
        print(request.data)
         
        email = global_session_data['user_name']
        employee = Employee.objects.get(email=email)
        today = timezone.now().date()
        date = request.data.get('date')
        print("the date is",date)
        billing_objects = Billing.objects.filter(employee=employee, date=date)
        serializer = BillingSerializer(billing_objects,many=True)
        return Response(serializer.data)

    def post(self,request):
        email = global_session_data['user_name']
        employee = Employee.objects.get(email=email)
        data =  request.data
        today = timezone.now().date()
        if Billing.objects.filter(Q(employee=employee,date=today)).exists():
            print("inside if")
            billing_object = Billing.objects.get(employee=employee, date=today)
            serializer = BillingSerializer(billing_object,data=request.data,partial=True)
            if serializer.is_valid():
                print("inside above serialiZer")
                serializer.save()
                return Response("Data Updated saved SUccessfully")

            else:
                print("first else")
                print(serializer.errors)
                return Response(serializer.errors,status=401)
        else:
            print("second else")
            request.data['employee'] = employee.pk
            serializer = BillingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response("data created")

            else:
                print("third else")
                print(serializer.errors)
                return Response(serializer.errors,status=400)
        
class PendingProjects(APIView):

    permission_classes = [IsAuthenticatedSession]
    def get(self,request,statuss):
        email =  global_session_data['user_name']
        EO =  Employee.objects.get(email=email)
        # statuss = request.data.get('status')
        tasks = TaskAssignToEmployee.objects.filter(employee=EO)
        data = []
        for project in tasks:
            PO = Project.objects.get(id=project.task_name.id)
        
            if statuss in PO.status:
                print(PO.task_name)

            # created_by , assigned date, status 
                if PO.created_by.name:

                    data.append({'task_name':PO.task_name,'pid':PO.id,'created_date':PO.created_date,'due_date':PO.due_date,'status':PO.status,'created_by':PO.created_by.name,'remarks':PO.remarks})
                else:
                    data.append({'task_name':PO.task_name,'pid':PO.id,'created__date':PO.created_date,'due_date':PO.due_date,'status':PO.status,'created_by':PO.assigned_by.name,'remarks':PO.remarks})


        return Response(data)
        serializer = UserTaskSerializer(tasks,context={'request':request},many=True)
        # return Response(serializer.data)


from datetime import datetime

class DisplayTaskFromDatetoDate(APIView):
    permission_classes = [IsAuthenticatedSession]
    def post(self, request):
        # Retrieve starting date and ending date from request data
        starting_date_str = request.data.get('starting_date')
        ending_date_str = request.data.get('ending_date')

        # Convert starting date and ending date strings to datetime objects
        starting_date = datetime.strptime(starting_date_str, '%Y-%m-%d').date()
        ending_date = datetime.strptime(ending_date_str, '%Y-%m-%d').date()
        eo =Employee.objects.get(email=global_session_data['user_name'])
        # Filter ActivitySheet objects based on the date range
        daily_activity_sheets = ActivitySheet.objects.filter(employee=eo,date__range=(starting_date, ending_date))

        # Serialize the queryset or process it further as needed
        # For example, you can serialize the queryset and return the data
        serializer = DailyActivitySheetSerializer(daily_activity_sheets, many=True,context={'request':request})
        return Response(serializer.data)

from django.contrib.auth.hashers import make_password
def fun():
    # Assuming you have a plain text password
    plain_text_password = 'irayya'

    # Hash the password
    hashed_password = make_password(plain_text_password)
    return hashed_password
# Now you can use the hashed password, for example, save it to the database


class AdminEmployees(APIView):
    permission_classes = [IsAuthenticatedSession]
    
    def get(self, request):
        
        email = global_session_data.get('user_name')
        EO = Employee.objects.get(email=email)
        
        if EO.status == 'admin':

            employees = Employee.objects.all()
        
            serializer = EmployeeDisplaySerializer(employees, many=True, context={'request': request})
        
            return Response(serializer.data)

        elif  EO.status =='manager':

            EO = Employee.objects.filter(reporting_to=EO)
        
            serializer = EmployeeDisplaySerializer(EO, many=True, context={'request': request})

            return Response(serializer.data)
        
        elif EO.status == 'team_leader':
            
            EO = Employee.objects.filter(team_leader=EO)
            
            serializer = EmployeeDisplaySerializer(EO, many=True, context={'request': request})

            return Response(serializer.data)

            
        else:

            return Response("you are not a admin")


from rest_framework.viewsets import ModelViewSet

class AllTasks(ModelViewSet):
    permission_classes  = [IsAuthenticatedSession]
    queryset = Project.objects.all()
    serializer_class =  ProjectSerializer

    def create(self, request, *args, **kwargs):

        coming_data =  request.data
        email =  global_session_data['user_name']
        EO =  Employee.objects.get(email=email)
        coming_data['created_by'] = EO

        serializer = self.serializer_class(data=coming_data)        
        
        if serializer.is_valid():
            # Perform additional operations before saving if needed
            # For example, you can set the created_by field here

            # Save the object
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProjectCreate(APIView):
    def post(self,request): 

        email = global_session_data['user_name']
        EO  =  Employee.objects.get(email=email)
        request.data['created_by'] =  EO.pk
        serializer = ProjectCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("dome")
        else:
            return Response(serializer.errors)
    
class DisplayProjects(APIView):
    permission_classes = [IsAuthenticatedSession]
    def get(self,request,status):

        PO = Project.objects.filter(status__icontains=status)

        serializer =  ProjectSerializer(PO,many=True,context={'request':request})
        return Response(serializer.data)

class DisplayParticularUserTasks(APIView):
    # def get(self,request,id):
    #     EO = Employee.objects.get(id=id)
    #     TO = TaskAssignToEmployee.objects.filter(__assigned_to=EO)
    #     print(TO)
    #     projects = []
    #     for i in TO:
    #         pid = i.task_name.id
    #         PO = Project.objects.get(id=pid)
    #         print(pid,PO)
    #         print(ProjectSerializer(PO,context={'request':request}).data)
    #         projects.append(ProjectSerializer(PO,context={'request':request}).data)
        
    #     return Response(projects)
    def get(self, request, id):
        # Get the employee object based on the provided ID
        employee = Employee.objects.get(id=id)
        
        # Filter tasks assigned to the specified employee
        tasks = TaskAssignToEmployee.objects.filter(employee=employee)
        
        # Serialize the projects associated with the tasks
        projects = []
        for task in tasks:
            project_data = ProjectCreateSerializer(task.task_name, context={'request': request}).data
            project_data['assigned_to']=employee.name
            projects.append(project_data)

        return Response(projects)

def passwordManagement(email,password):
    try:
        employee = Employee.objects.get(email=email)
    except Employee.DoesNotExist:
        raise NotFound("Employee not found")

    
    hashed_password = make_password(password)
    
    employee.password = hashed_password
    employee.save()
    
    return Response("Password changed successfully", status=200)


def send_otp(email):
    otp =''
    for i in range(6):
        otp+= str(random.randrange(0,9))

    send_mail(
        "OTP for CHanging Password",
        f"your OTP to change the password is {otp}",
        "kalamallarajasekhar256@gmail.com",
        [email],
        fail_silently=False

    )
    return otp   

class ChangePassword(APIView):
    permission_classes = [IsAuthenticatedSession]
    def get(self,request):
        email = global_session_data['user_name']
        otp = send_otp(email)
        print(otp)
        return Response({'message':"OTP sent Successfully",'OTP':otp})


    def post(self, request):
        try:
            email = global_session_data['user_name']
            password = request.data.get('password')

            return passwordManagement(email,password)

        except Employee.DoesNotExist:
            raise NotFound("Employee not found")


class ForgetPassword(APIView):
    def post(self,request,email):
        
        if Employee.objects.filter(email=email).exists():
            otp = send_otp(email)
            print(otp)     
            return Response({'message':"OTP sent Successfully",'OTP':otp})
        else:
            return Response({'message':"UnAuthorized Email"},status=401)



    def put(self, request,email):
        try:
            # email = global_session_data['user_name']
            password = request.data.get('password')

            return passwordManagement(email,password)

        except Employee.DoesNotExist:
            raise NotFound("Employee not found")

#generate otp
import random

def generate_otp():
    otp = ''
    for i in range(6):  
        otp += str(random.randint(0, 9))
    return otp

    
# class ForgetPassword(APIView):
#     def post(self,request):

#         email  =  request.data.get('email')
#         try:
#             EO = Employee.objects.get(email=email)
#         except Exception as e:
#             return Response("email is not registered yet")
#         otp = generate_otp()
#         send_mail(
#             "OTP Verification For Reset the password",
#             f"Don't share this OTP with anyone your OTP is {otp}",
#             "kalamallarajasekhar256#gmail.com",
#             [email],
#             fail_silently=False
#         )
#         if OTP.objects.filter(employee=EO,otp=otp).exists():
#             OTPO = OTP.objects.get(employee=EO,otp=otp)
#             OTPO.update(otp=otp)
#         else:

#             OTP.objects.create(employee=EO,otp=otp)
#         return Response("mail sent succesfully")


#     def put(self,request):

#         email = request.data.get('email')
#         password =  request.data.get(pw)
#         enterred_otp =  request.data.get('otp')
#         EmployeeOtpObject = OTP.objects.get(employee=Employee.objects.get(email=email))

#         if EmployeeOtpObject.otp == enterred_otp:
#             return passwordManagement(email,password)
#         else:
#             return Response("Invalid OTP")
        

class TaskAssignToEmployeeView(APIView):
    permission_classes = [IsAuthenticatedSession]
    def post(self,request):
        email  =  global_session_data['user_name']  
        managersObject = Employee.objects.get(email=email)
        # position = EO.status
        employee_id = request.data.get('employee_id')
        EO = Employee.objects.get(id=employee_id)

        project_id = request.data.get('project_id')
        PO = Project.objects.get(id= project_id)
        request.data['created_by'] = managersObject
        request.data['employee'] = EO
        request.data['task_name'] = PO
        serializer = TaskAssignToEmployeeUpdateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response("data saved sucessfully")
        else:
            print(serializer.errors)
            return Response(serializer.errors)


class ProjectAssign(APIView):
    def post(self,request):
        assign_by = global_session_data['user_name']
        try:

            admin = Employee.objects.get(email=assign_by)

            empid = request.data.get('employee_id') 
            pid =  request.data.get('project_id')
            EO =  Employee.objects.get(id =empid)
            PO = Project.objects.get(id=pid)

            TaskAssignToEmployee.objects.create(created_by=admin,task_name=PO,employee=EO)
            return Response("Project Assigned successfully")
        except Exception as e:
            print(e)
            return Response(e)
class DisplayEmployeeProjects(APIView):
    def get(self, request, employee_id):
        try:
            # Get the employee object
            EO = Employee.objects.get(id=employee_id)
            # Get employees who report to the specified employee
            PEO = Employee.objects.filter(reporting_to=EO)
            print("the employees",PEO)
            # Get tasks assigned to employees who report to the specified employee
            TAEO = TaskAssignToEmployee.objects.filter(employee__in=PEO)
            # Serialize the tasks
            send_data = []
            for project in TAEO:
                print(project.task_name.id)

                PO = Project.objects.get(id=project.task_name.id)
                serializer = ProjectSerializer(PO,context={'request':request})
                send_data.append(serializer.data)
        
            
            return Response(send_data)
        except Employee.DoesNotExist:
            return Response("Employee not found")


class ReportingEmployees(APIView):
    def get(self,request,employee_id):
        EO  =  Employee.objects.get(id=employee_id)

        employee_objects = Employee.objects.filter(reporting_to=EO)
        serializer =  EmployeeDisplaySerializer(employee_objects,many=True,context={'request':request}).data
        for employee in serializer:
            if Employee.objects.filter(reporting_to=employee['pk']).exists():
                employee['reporters'] = True
            else:
                employee['reporters'] = False

        return Response(serializer)


