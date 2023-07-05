from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Experience
from .serializers import ExperienceSerializer


class ExperienceList(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Experience.objects.annotate(
        recommendations_count=Count('recommendations', distinct=True),
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'profile',
        'company',
        'recommendations__profile',
    ]
    search_fields = [
        'title',
        'company_name',
        'profile__owner__username',
    ]
    ordering_fields = [
        'recommendations_count',
        'recommendations__created_at',
        'is_current',
    ]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Experience.objects.annotate(
        recommendations_count=Count('recommendations', distinct=True),
    ).order_by('-created_at')
