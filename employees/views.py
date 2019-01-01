from rest_framework import viewsets
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import permissions
from .permissions import IsCompanyAdmin, IsSuperAdmin, IsUserSelf
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

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

    @action(detail=True, methods=['post'], name='Invite to Team')
    def invite_to_team(self, request, pk=None):
        emp_id = request.data['emp_id']
        team_id = request.data['team_id']

        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            return Response(data='Invalid employee id.', status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(data='Invalid team id.', status=status.HTTP_400_BAD_REQUEST)


        return Response(data='Employee invited to team.', status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], name='Invite to Company')
    def invite_to_company(self, request, pk=None):
        emp_id = request.data['emp_id']
        company_from = request.data['company_from']

        # TODO: Validate schema name
        with schema_context(company_from):
            try:
                employee = Employee.objects.get(id=emp_id)
            except Employee.DoesNotExist:
                return Response(data='Invalid employee id.', status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Employee invited to company.', status=status.HTTP_200_OK)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('create', 'destroy', 'list', 'invite_to_team'):
            permission_classes = [permissions.IsAuthenticated, IsCompanyAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsUserSelf]

        return [permission() for permission in permission_classes]
