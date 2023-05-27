from django.urls import path
from relationships import views

urlpatterns = [
    path('relationships/', views.RelationshipList.as_view()),
    path('relationships/<int:pk>/', views.RelationshipDetail.as_view()),
]
