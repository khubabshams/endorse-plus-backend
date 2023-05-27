from django.db.models import Q
from django.db import IntegrityError
from rest_framework import serializers
from .models import Request
from profiles.models import Profile


class RequestSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')

    class Meta:
        model = Request
        fields = [
            'id', 'profile', 'receiver', 'created_at', 'seen', 'message',
        ]

    def __init__(self, *args, **kwargs):
        """
        override init to filter the queryset of receiver,
        should not contain sender (request user) record
        """
        super(RequestSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user

        self.fields['receiver'].queryset = Profile.objects.\
            filter(~Q(owner=request_user))

    def create(sefl, validated_data):
        """
        override create to handle record duplication error
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(({
                'error_message':
                'You cannot send recommendation request to same person twice!',
            }))
