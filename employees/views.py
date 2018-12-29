from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import permissions
from .permissions import IsCompanyAdmin, IsSuperAdmin, IsUserSelf
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #permission_classes = (permissions.IsAuthenticated, IsCompanyAdminOrUser) 

    def create(self, request):
        name = request.data['name']
        #schema_name = request.data['schema_name']
        user = User.objects.create_user(username=name, password='test1234')
        #is_company_admin = False
        #num_users = User.objects.filter().count()
        #if num_users == 1:
        #    is_company_admin = True
        #employee = Employee(name='company_admin', is_company_admin=True, company=company, user=user)
        employee = Employee(name=name, user=user)
        employee.save()

        return Response(status=status.HTTP_201_CREATED)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('create', 'destroy', 'list'):
            permission_classes = [permissions.IsAuthenticated, IsCompanyAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsUserSelf]

        return [permission() for permission in permission_classes]
