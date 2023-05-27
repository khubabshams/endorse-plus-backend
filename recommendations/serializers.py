from rest_framework import serializers
from .models import Recommendation


class RecommendationSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Recommendation
        fields = [
            'id', 'profile', 'created_at', 'updated_at', 'receiver', 'content',
            'is_featured', 'related_experience', 'relation', 'boosts'
        ]
