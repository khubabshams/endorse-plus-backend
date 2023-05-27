from rest_framework import serializers
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return user == obj.profile.owner

    class Meta:
        model = Recommendation
        fields = [
            'id', 'profile', 'created_at', 'updated_at', 'receiver', 'content',
            'is_featured', 'related_experience', 'relation', 'boosts',
            'is_owner'
        ]
