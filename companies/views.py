from rest_framework import viewsets
from .models import Company
from .serializers import CompanySerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from tenant_schemas.utils import schema_context
from employees.models import Employee
from django.conf import settings

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows company to be viewed or edited.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAdminUser,) 

    def create(self, request):
        name = request.data['name']
        address = request.data['address']
        if Company.objects.filter(name=name).exists():
            return Response(data='Companay with the same name already exists.', status=status.HTTP_400_BAD_REQUEST)

        schema_name = name
        domain_url = name + settings.DOMAIN_NAME
        company = Company(name=name, schema_name=schema_name, domain_url=domain_url, 
                address=address)
        company.auto_drop_schema = True
        company.save()

        with schema_context(company.schema_name):
            user = User.objects.create_user(username='company_admin', password='test1234')
            employee = Employee(name='company_admin', is_company_admin=True, user=user)
            employee.save()

        return Response(data='Company successfully created.', status=status.HTTP_201_CREATED)
