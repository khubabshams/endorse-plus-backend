from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Experience
from .serializers import ExperienceSerializer


class ExperienceList(generics.ListCreateAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Experience.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class ExperienceDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Experience.objects.all()
