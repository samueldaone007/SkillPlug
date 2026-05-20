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
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
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
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Style the inputs
        self.fields['username'].widget.attrs['placeholder'] = 'Username or Email'
        self.fields['username'].widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'

class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm
    template_name = 'accounts/login.html'