from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_company_admin = models.BooleanField(default=False)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    #joining_date = models.DateTimeField(default=datetime.now)
    #address = models.CharField(max_length=200)

class Team(models.Model):
    name = models.CharField(max_length=100)
