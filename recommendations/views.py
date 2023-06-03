from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Recommendation
from .serializers import RecommendationSerializer


class RecommendationList(generics.ListCreateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recommendation.objects.annotate(
        boosts_count=Count('boosts', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'profile',
        'receiver',
        'is_featured',
        'boosts__profile',
    ]
    search_fields = [
        'profile__owner__username',
        'receiver__owner__username',
        'related_experience__title',
    ]
    ordering_fields = [
        'boosts_count',
        'boosts__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class RecommendationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Recommendation.objects.annotate(
        boosts_count=Count('boosts', distinct=True),
    ).order_by('-created_at')
