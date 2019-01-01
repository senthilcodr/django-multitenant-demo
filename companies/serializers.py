from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    num_employees = serializers.SerializerMethodField()

    def get_num_employees(self, company):
        return company.get_num_employees()

    class Meta:
        model = Company
        fields = ('id', 'name', 'address', 'num_employees')
        extra_kwargs = {
                        'name': {'required': True}, 
                        'address': {'required': True},
                        }
