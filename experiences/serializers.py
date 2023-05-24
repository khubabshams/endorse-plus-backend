from rest_framework import serializers
from .models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Experience
        fields = [
            'id', 'profile', 'created_at', 'updated_at', 'title',
            'location', 'date_from', 'date_to', 'is_current', 'description'
        ]
