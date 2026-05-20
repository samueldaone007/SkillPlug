from django.urls import path
from . import views

urlpatterns = [
    path('', views.MarketplaceView.as_view(), name='marketplace_list'),
    path('<int:pk>/', views.FreelancerDetailView.as_view(), name='freelancer_detail'),
]
