from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import IntegrityError
from rest_framework import serializers
from .models import Request
from profiles.models import Profile


class RequestSerializer(serializers.ModelSerializer):
    receiver_name = serializers.ReadOnlyField(source='receiver.name')
    profile_name = serializers.ReadOnlyField(source='profile.name')
    receiver_title = serializers.ReadOnlyField(source='receiver.title')
    profile_title = serializers.ReadOnlyField(source='profile.title')
    receiver_image = serializers.ReadOnlyField(source='receiver.image.url')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    is_owner = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return user == obj.profile.owner

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    class Meta:
        model = Request
        fields = [
            'id', 'profile', 'receiver', 'created_at', 'seen', 'message',
            'is_owner', 'profile_name', 'receiver_name', 'profile_title',
            'receiver_title', 'receiver_image', 'profile_image'
        ]

    def __init__(self, *args, **kwargs):
        """
        override init to filter the queryset of receiver,
        should not contain sender (request user) record
        """
        super(RequestSerializer, self).__init__(*args, **kwargs)
        request_user = self.context['request'].user
        if request_user.id:
            self.fields['receiver'].queryset = Profile.objects.\
                filter(~Q(owner=request_user))

    def create(self, validated_data):
        """
        override create to handle record duplication error
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(({
                'detail':
                'You cannot send recommendation request to same person twice!',
            }))


class RequestSeenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['seen']

    def update(self, instance, validated_data):
        """
        override update to ensure only receiver is able to change seen flag
        """
        if instance.receiver != self.context['request'].user.profile:
            raise serializers.ValidationError(({
                'detail':
                ('Only the receiver can update this request!'),
            }))
        instance.seen = validated_data.get('seen', False)
        instance.save()
        return instance
