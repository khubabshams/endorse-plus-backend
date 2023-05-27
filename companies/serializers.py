from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'archive', 'created_at', 'updated_at', 'description'
        ]
