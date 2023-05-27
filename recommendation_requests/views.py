from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Request
from .serializers import RequestSerializer


class RequestList(generics.ListCreateAPIView):
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Request.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RequestSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Request.objects.all()
