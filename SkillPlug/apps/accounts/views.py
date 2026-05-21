from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import UserSignupForm, ProfileEditForm
from .models import CustomUser, Profile
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class SignupView(CreateView):
    form_class = UserSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.skills.set(form.cleaned_data.get('skills', []))
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio_items'] = self.request.user.portfolio_items.all().order_by('-created_at')
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileEditForm
    template_name = 'accounts/edit_profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Pre-populate skills from Profile so checkboxes show current state
        try:
            form.fields['skills'].initial = self.request.user.profile.skills.all()
        except Profile.DoesNotExist:
            pass
        return form

    def form_valid(self, form):
        # Save user fields (full_name, bio, school, etc.)
        response = super().form_valid(form)
        # Save skills to Profile (ManyToMany) — this was missing before
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        profile.skills.set(form.cleaned_data.get('skills', []))
        # Update whatsapp_link
        if self.request.user.whatsapp:
            profile.whatsapp_link = "https://wa.me/{}".format(
                self.request.user.whatsapp.replace('+', '').replace(' ', '')
            )
            profile.save()
        return response


class ProfileDetailView(DetailView):
    model = CustomUser
    template_name = 'accounts/profile_detail.html'
    context_object_name = 'profile_user'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('profile', 'profile__skills')


class CustomAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username or Email'
        self.fields['username'].widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].widget.attrs['class'] = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 outline-none'

class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm
    template_name = 'accounts/login.html'