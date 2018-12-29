from django.db import models
#from django.contrib.auth.models import User
from datetime import datetime
from tenant_schemas.models import TenantMixin

class Company(TenantMixin):
    name = models.CharField(max_length=100)
    #admin = models.OneToOneField(User, on_delete=models.CASCADE)
    #date_of_incorporation = models.DateTimeField(default=datetime.now)
    #address = models.CharField(max_length=200)

