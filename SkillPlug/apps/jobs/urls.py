from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='jobs_list'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<int:pk>/apply/', views.JobApplyView.as_view(), name='job_apply'),
]