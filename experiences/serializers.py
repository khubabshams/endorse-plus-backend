from rest_framework import serializers
from .models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    profile_name = serializers.ReadOnlyField(source='profile.name')
    is_owner = serializers.SerializerMethodField()
    recommendations_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return user == obj.profile.owner

    class Meta:
        model = Experience
        fields = [
            'id', 'profile', 'created_at', 'updated_at', 'title', 'company',
            'location', 'date_from', 'date_to', 'is_current', 'description',
            'recommendations', 'is_owner', 'recommendations_count',
            'profile_name'
        ]
