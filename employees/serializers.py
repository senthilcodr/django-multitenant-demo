from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'name','address')
        read_only_fields = ('id',)
        extra_kwargs = {
                        'name': {'required': True}, 
                        'address': {'required': True},
                        }

