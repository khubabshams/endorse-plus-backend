from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'name',
            'linkedin_profile_url', 'summary', 'image', 'requests_sent',
            'requests_received', 'recommendations_sent',
            'recommendations_received', 'boosts'
        ]
