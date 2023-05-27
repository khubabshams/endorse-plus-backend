from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Company.objects.all()


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Company.objects.all()
