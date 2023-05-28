from django.db.models import Q
from django.db import IntegrityError
from rest_framework import serializers
from .models import Recommendation
from boosts.models import Boost
from profiles.models import Profile
from experiences.models import Experience


class RecommendationSerializer(serializers.ModelSerializer):
    profile = serializers.ReadOnlyField(source='profile.owner.username')
    is_owner = serializers.SerializerMethodField()
    boost_id = serializers.SerializerMethodField()
    boosts_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        user = self.context['request'].user
        return user == obj.profile.owner

    def get_boost_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            boost = Boost.objects.filter(profile=user.profile,
                                         recommendation=obj).first()
            return boost and boost.id or None
        return None

    class Meta:
        model = Recommendation
        fields = [
            'id', 'profile', 'created_at', 'updated_at', 'receiver', 'content',
            'is_featured', 'related_experience', 'relation', 'boosts',
            'is_owner', 'boost_id', 'boosts_count'
        ]

    def __init__(self, *args, **kwargs):
        """
        override init to filter the queryset of receiver
        to not be same as sender, and experience to be one of receivers'
        """
        super(RecommendationSerializer, self).__init__(*args, **kwargs)
        user = self.context['request'].user
        if user.is_authenticated:
            self.fields['receiver'].queryset = Profile.objects.\
                filter(~Q(owner=user))

    def validate_receiver_experience(self, validated_data):
        user_experiences = validated_data['receiver'].experiences.all()
        if validated_data['related_experience'] not in user_experiences:
            raise serializers.ValidationError(({
                'detail':
                    'You can recommend user only on his own experiences!'
            }))

    def create(self, validated_data):
        """
        override create to handle duplication and
        not relevant experience errors
        """
        self.validate_receiver_experience(validated_data=validated_data)

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(({
                'detail':
                ('You have recommended this user for the same experience'
                 ' before!'),
            }))

    def update(self, instance, validated_data):
        """
        override update to handle duplication and
        not relevant experience errors
        """
        self.validate_receiver_experience(validated_data=validated_data)

        try:
            instance.save()
            return instance
        except IntegrityError:
            raise serializers.ValidationError(({
                'detail':
                ('You have recommended this user for the same experience'
                 ' before!'),
            }))
