from django.urls import path
from recommendation_requests import views

urlpatterns = [
    path('requests/', views.RequestList.as_view()),
    path('requests/<int:pk>/', views.RequestDetail.as_view()),
    path('requests/seen/<int:pk>/', views.RequestSeen.as_view()),
]
