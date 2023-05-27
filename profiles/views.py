from django.db.models import Count
from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListCreateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Profile.objects.annotate(
        recommendations_sent_count=Count('recommendations_sent',
                                         distinct=True),
        recommendations_received_count=Count('recommendations_received',
                                             distinct=True),
        requests_sent_count=Count('requests_sent', distinct=True),
        requests_received_count=Count('requests_received', distinct=True),
        boosts_count=Count('boosts', distinct=True),
    ).order_by('-created_at')


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
