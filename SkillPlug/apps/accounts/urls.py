from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Make sure this 'dashboard' path exists
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('signup/', views.SignupView.as_view(), name='account_signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        next_page='/profiles/dashboard/'
    ), name='account_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='account_logout'),
    path('dashboard/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),
]