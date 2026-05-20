from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserSignupForm, ProfileEditForm
from .models import CustomUser, Profile

class SignupView(CreateView):
    form_class = UserSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('profile_edit')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        Profile.objects.get_or_create(user=user)
        return super().form_valid(form)

class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('profile_edit')

    def get_object(self):
        return self.request.user

class ProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('profile', 'profile__skills')
