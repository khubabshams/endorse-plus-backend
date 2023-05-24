from rest_framework import generics, permissions
from endorse_plus_backend.permissions import IsOwnerOrReadonly
from .models import Company
from .serializers import CompanySerializer


class CompanyList(generics.ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Company.objects.all()

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsOwnerOrReadonly]
    queryset = Company.objects.all()
