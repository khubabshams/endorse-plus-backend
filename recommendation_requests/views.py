from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from endorse_plus_backend.permissions import IsOwnerOrReceiver
from .models import Request
from .serializers import RequestSerializer, RequestSeenSerializer


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Request.objects.all()
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
    ]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsOwnerOrReceiver]
    queryset = Request.objects.all()


class RequestSeen(generics.RetrieveUpdateAPIView):
    serializer_class = RequestSeenSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Request.objects.all()
