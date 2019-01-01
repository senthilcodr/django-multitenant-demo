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
        try:
            company = Company(name=name, schema_name=schema_name, domain_url=domain_url, 
                    address=address)
            # This option does not seem to work.  The schemas are not deleted when company is deleted.
            company.auto_drop_schema = True
            company.save()
        except Exception as e:
            return Response(data='Unable to create Companay with the given input.', status=status.HTTP_400_BAD_REQUEST)

        # Create company admin user in the tenant/company schema
        with schema_context(company.schema_name):
            company_admin_name = company.schema_name + '_admin'
            user = User.objects.create_user(username=company_admin_name, password='test1234')
            employee = Employee(name=company_admin_name, is_company_admin=True, user=user)
            employee.save()

        return Response(data='Company successfully created.', status=status.HTTP_201_CREATED)
