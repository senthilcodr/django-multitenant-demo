from django.db import models
from datetime import date
from tenant_schemas.models import TenantMixin
from tenant_schemas.utils import schema_context
from employees.models import Employee

class Company(TenantMixin):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def get_num_employees(self):
        with schema_context(self.schema_name):
            return Employee.objects.count()

