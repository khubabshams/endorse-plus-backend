from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Company
        fields = [
            'id', 'profile', 'name', 'created_at', 'updated_at', 'description'
        ]
