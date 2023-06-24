from rest_framework import serializers
from .models import Profile
from recommendation_requests.models import Request


class ProfileSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()
    unseen_requests_count = serializers.SerializerMethodField()
    recommendations_sent_count = serializers.ReadOnlyField()
    recommendations_received_count = serializers.ReadOnlyField()
    requests_sent_count = serializers.ReadOnlyField()
    requests_received_count = serializers.ReadOnlyField()
    boosts_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_unseen_requests_count(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Request.objects.filter(seen=False, profile=user.profile).\
                count()
        return 0

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'title', 'created_at', 'updated_at',
            'linkedin_profile_url', 'summary', 'image', 'requests_sent',
            'requests_received', 'recommendations_sent',
            'recommendations_received', 'boosts', 'is_owner',
            'unseen_requests_count', 'recommendations_sent_count',
            'experiences', 'recommendations_received_count',
            'requests_sent_count', 'requests_received_count', 'boosts_count'
        ]
