from rest_framework import permissions
from django.db import connection
from .models import Employee

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        #print(connection.get_tenant())
        return connection.get_tenant() == 'public' and permissions.IsAdminUser(request.user)

class IsCompanyAdmin(permissions.BasePermission):
    """
    Custom permission to only allow company admin users to create/destroy employees.
    """

    def has_permission(self, request, view):
        try:
            employee = Employee.objects.get(user__id=request.user.id)
        except Employee.DoesNotExist:
            return False
        return employee.is_company_admin

class IsSameCompany(permissions.BasePermission):
    """
    Custom permission to only allow same company users.
    """

    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(user__id=obj.user.id)
        except Employee.DoesNotExist:
            return False

        try:
            request_employee = Employee.objects.get(user__id=request.user.id)
        except Employee.DoesNotExist:
            return False

        return employee.is_company_admin

class IsUserSelf(permissions.BasePermission):
    """
    Custom permission to only allow same users to edit the the profile.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
        if obj.user.id == request.user.id:
            if request.method in ('GET','POST'):
                return True
        else:
            try:
                employee = Employee.objects.get(user__id=request.user.id)
            except Employee.DoesNotExist:
                return False
            if employee.is_company_admin and request.method in ('GET', 'POST', 'DELETE'):
                return True

        return False
