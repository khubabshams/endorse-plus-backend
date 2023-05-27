from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsAdminOrReadOnly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Company.objects.filter(archive=False)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Company.objects.filter(archive=False)
