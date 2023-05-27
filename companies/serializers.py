from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'created_at', 'updated_at', 'description'
        ]


class RelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'created_at', 'updated_at', 'description'
        ]
