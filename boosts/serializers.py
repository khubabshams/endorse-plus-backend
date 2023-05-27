from django.db.models import Q
from django.db import IntegrityError
from rest_framework import serializers
from .models import Boost
from profiles.models import Profile


class BoostSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Boost
        fields = [
            'id', 'profile', 'created_at', 'recommendation',
        ]

    def create(sefl, validated_data):
        """
        override create to handle record duplication error
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(({
                'detail': 'You cannot boost the same recommendation twice!',
            }))
