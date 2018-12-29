from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        #fields = ('name','schema_name', 'domain_url')
        fields = ('name',)

