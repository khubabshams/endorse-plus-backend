from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.annotate(
        recommendations_sent_count=Count('recommendations_sent',
                                         distinct=True),
        recommendations_received_count=Count('recommendations_received',
                                             distinct=True),
        requests_sent_count=Count('requests_sent', distinct=True),
        requests_received_count=Count('requests_received', distinct=True),
        boosts_count=Count('boosts', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner',
        'requests_sent__profile',
        'requests_received__profile',
        'recommendations_sent__profile',
        'recommendations_received__profile',
        'boosts__profile',
    ]
    search_fields = [
        'profile__owner__username',
    ]
    ordering_fields = [
        'recommendations_sent_count',
        'recommendations_received_count',
        'requests_sent_count',
        'requests_received_count',
        'boosts_count',
        'recommendations_received__created_at',
        'boosts__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Profile.objects.annotate(
        recommendations_sent_count=Count('recommendations_sent',
                                         distinct=True),
        recommendations_received_count=Count('recommendations_received',
                                             distinct=True),
        requests_sent_count=Count('requests_sent', distinct=True),
        requests_received_count=Count('requests_received', distinct=True),
    ).order_by('-created_at')
