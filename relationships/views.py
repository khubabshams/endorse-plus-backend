from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsAdminOrReadOnly
from .models import Relationship
from .serializers import RelationshipSerializer


class RelationshipList(generics.ListCreateAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Relationship.objects.filter(archive=False)


class RelationshipDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Relationship.objects.filter(archive=False)
