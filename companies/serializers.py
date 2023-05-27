from rest_framework import serializers
from .models import Company, Relationship


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = [
            'id', 'name', 'archive', 'created_at', 'updated_at', 'description'
        ]


class RelationshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relationship
        fields = [
            'id', 'name', 'archive', 'created_at'
        ]
