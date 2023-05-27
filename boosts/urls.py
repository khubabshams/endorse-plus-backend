from django.urls import path
from boosts import views

urlpatterns = [
    path('boosts/', views.BoostList.as_view()),
    path('boosts/<int:pk>/', views.BoostDetail.as_view()),
]
