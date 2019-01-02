from rest_framework import viewsets
from .models import Employee, Team
from .serializers import EmployeeSerializer, TeamSerializer
from rest_framework import permissions
from .permissions import IsCompanyAdmin, IsUserSelf
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from tenant_schemas.utils import schema_context
from companies.models import Company
from tenant_schemas.utils import get_public_schema_name
from django.db import connection

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    def create(self, request):
        name = request.data['name']
        address = request.data['address']
            
        user = User.objects.create_user(username=name, password='test1234')
        employee = Employee(name=name, user=user, address=address)
        employee.save()

        return Response(data="Employee successfully added.", status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=['post'], name='Invite to Team')
    def invite_to_team(self, request, pk):
        employee = self.get_object()
        if 'team_id' in request.data:
            team_id = request.data['team_id']
        else:
            return Response(data="Required parameter 'team_id' is missing", status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(data='Invalid team id.', status=status.HTTP_400_BAD_REQUEST)

        if employee.belonging_team and employee.belonging_team.id == team.id:
            return Response(data='Employee already belongs to this team.', status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Employee invited to team.', status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], name='Invite to Company')
    def invite_to_company(self, request):
        if 'emp_id' in request.data:
            emp_id = request.data['emp_id']
        else:
            return Response(data="Required parameter 'emp_id' is missing", status=status.HTTP_400_BAD_REQUEST)

        if 'company_from' in request.data:
            company_from = request.data['company_from']
        else:
            return Response(data="Required parameter 'company_from' is missing", status=status.HTTP_400_BAD_REQUEST)

        if company_from == connection.schema_name:
            return Response(data='Cannot invite employee from same company.', status=status.HTTP_400_BAD_REQUEST)

        with schema_context(get_public_schema_name()):
            if not Company.objects.filter(name=company_from).exists():
                return Response(data='Invalid company name.', status=status.HTTP_400_BAD_REQUEST)

        with schema_context(company_from):
            try:
                employee = Employee.objects.get(id=emp_id)
            except Employee.DoesNotExist:
                return Response(data='Invalid employee id.', status=status.HTTP_400_BAD_REQUEST)

        return Response(data='Employee invited to company.', status=status.HTTP_200_OK)


    def get_permissions(self):
        if self.action in ('create', 'destroy', 'list', 'invite_to_team', 'invite_to_company'):
            permission_classes = [permissions.IsAuthenticated, IsCompanyAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated, IsUserSelf]

        return [permission() for permission in permission_classes]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def create(self, request):
        name = request.data['name']
        manager_id = request.data['manager_id']

        try:
            manager = Employee.objects.get(id=manager_id)
            if manager.belonging_team:
                return Response(data='Manager belongs to different team.', status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response(data='Invalid manager id.', status=status.HTTP_400_BAD_REQUEST)

        team = Team(name=name, manager=manager)
        team.save()

        manager.belonging_team = team
        manager.save()

        return Response(data="Team successfully created.", status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.action in ('list',):
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsCompanyAdmin]

        return [permission() for permission in permission_classes]

