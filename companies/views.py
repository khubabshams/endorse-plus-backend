from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsAdminOrReadOnly
from .models import Company, Relationship
from .serializers import CompanySerializer, RelationshipSerializer


class CompanyList(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Company.objects.filter(archive=False)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Company.objects.filter(archive=False)


class RelationshipList(generics.ListCreateAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Relationship.objects.filter(archive=False)


class RelationshipDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RelationshipSerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Relationship.objects.filter(archive=False)
