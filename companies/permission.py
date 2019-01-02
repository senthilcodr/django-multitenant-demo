from rest_framework import permissions


class IsCompanyAdminOrUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            if request.method in ('GET','POST'):
                return True
        else:
            employee = Employee.objects.get(user=request.user)
            if employee.is_company_admin and request.method in ('GET', 'POST', 'DELETE'):
                return True

        return False
