from rest_framework import permissions
from django.db import connection

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        #print(connection.get_tenant())
        return connection.get_tenant() == 'public' and permissions.IsAdminUser(request.user)

class IsCompanyAdmin(permissions.BasePermission):
    """
    Custom permission to only allow company admin users to create/destroy employees.
    """

    def has_permission(self, request, view):
        employee = Employee.objects.get(user=request.user)
        return employee.is_company_admin

class IsUserSelf(permissions.BasePermission):
    """
    Custom permission to only allow same users to edit the the profile.
    """

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            if request.method in ('GET','POST'):
                return True
        else:
            employee = Employee.objects.get(user=request.user)
            if employee.is_company_admin and request.method in ('GET', 'POST', 'DELETE'):
                return True

        return False
