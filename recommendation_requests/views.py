from rest_framework import generics, permissions, filters
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Request
from .serializers import RequestSerializer


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Request.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
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
    permission_classes = [IsOwnerOrReadonly]
    queryset = Request.objects.all()
