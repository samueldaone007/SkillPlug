from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('dashboard/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]