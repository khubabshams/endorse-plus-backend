from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Request
from django.db.models import Q
from .serializers import RequestSerializer, RequestSeenSerializer


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'profile',
        'receiver',
        'seen',
    ]
    search_fields = [
        'profile__owner__username',
        'receiver__owner__username',
        'message',
    ]
    ordering_fields = [
        'created_at',
        'seen',
    ]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Request.objects.\
            filter(Q(profile=user_profile) | Q(receiver=user_profile))


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsOwnerOrReadonly]

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Request.objects.\
            filter(Q(profile=user_profile) | Q(receiver=user_profile))


class RequestSeen(generics.RetrieveUpdateAPIView):
    serializer_class = RequestSeenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Request.objects.all()

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Request.objects.\
            filter(Q(profile=user_profile) | Q(receiver=user_profile))
