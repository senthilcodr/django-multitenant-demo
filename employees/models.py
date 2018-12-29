from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_company_admin = models.BooleanField(default=False)

    name = models.CharField(max_length=100)
    #joining_date = models.DateTimeField(default=datetime.now)
    #address = models.CharField(max_length=200)    

#class CompanyAdmin(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    company = models.ForeignKey(Company, on_delete=models.CASCADE)
