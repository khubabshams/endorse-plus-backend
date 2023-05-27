from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Recommendation
from .serializers import RecommendationSerializer


class RecommendationList(generics.ListCreateAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recommendation.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class RecommendationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecommendationSerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Recommendation.objects.all()
