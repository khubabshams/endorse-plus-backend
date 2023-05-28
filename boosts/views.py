from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Boost
from .serializers import BoostSerializer


class BoostList(generics.ListCreateAPIView):
    serializer_class = BoostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Boost.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class BoostDetail(generics.RetrieveDestroyAPIView):
    serializer_class = BoostSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Boost.objects.all()
