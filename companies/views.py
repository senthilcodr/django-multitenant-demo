from rest_framework import viewsets
from .models import Company, Employee
from .serializers import CompanySerializer, EmployeeSerializer
from rest_framework import permissions
from .permissions import IsCompanyAdmin, IsSuperAdmin
from django.contrib.auth.models import User
from tenant_schemas.utils import schema_context


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    #permission_classes = (IsSuperAdmin,) 
    permission_classes = (permissions.IsAdminUser,) 

    def create(self, request):
        name = request.data['name']
        schema_name = request.data['schema_name']
        domain_url = request.data['domain_url']
        company = Company(name=name, schema_name=schema_name, domain_url=domain_url)
        company.save()
        #with schema_context(company.schema_name):
        #    user = User.objects.create_user(username='company_admin', password='test1234')
        #    employee = Employee(name='company_admin', is_company_admin=True, company=company, user=user)
        #    employee.save()

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    #permission_classes = (permissions.IsAuthenticated, IsCompanyAdminOrUser) 

    def create(self, request):
        name = request.data['name']
        schema_name = request.data['schema_name']
        user = User.objects.create_user(username=name, password='test1234')
        is_company_admin = False
        num_users = User.objects.filter().count()
        if num_users == 1:
            is_company_admin = True
        employee = Employee(name='company_admin', is_company_admin=True, company=company, user=user)
        employee.save()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('create', 'destroy'):
            permission_classes = [IsCompanyAdmin]
        else:
            permission_classes = [IsUserSelf]
        return [permission() for permission in permission_classes]
