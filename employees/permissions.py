from rest_framework import permissions
from django.db import connection
from .models import Employee

class IsCompanyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            employee = Employee.objects.get(user__id=request.user.id)
        except Employee.DoesNotExist:
            return False
        return employee.is_company_admin


class IsUserSelf(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
