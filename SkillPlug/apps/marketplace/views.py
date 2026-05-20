from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Q
from apps.accounts.models import CustomUser, Skill, Profile
from apps.marketplace.models import PortfolioItem

class HomeView(ListView):
    model = CustomUser
    template_name = 'index.html'
    context_object_name = 'featured_freelancers'
    paginate_by = 6

    def get_queryset(self):
        return CustomUser.objects.filter(availability_status='available', verified=True).select_related('profile').prefetch_related('profile__skills')[:6]

class MarketplaceView(ListView):
    model = CustomUser
    template_name = 'marketplace/list.html'
    context_object_name = 'freelancers'
    paginate_by = 12

    def get_queryset(self):
        qs = CustomUser.objects.filter(verified=True).select_related('profile').prefetch_related('profile__skills')
        q = self.request.GET.get('q', '')
        school = self.request.GET.get('school', '')
        skill = self.request.GET.get('skill', '')
        availability = self.request.GET.get('availability', '')

        if q:
            qs = qs.filter(Q(full_name__icontains=q) | Q(profile__skills__name__icontains=q))
        if school and school != 'all':
            qs = qs.filter(school=school)
        if skill and skill != 'all':
            qs = qs.filter(profile__skills__id=skill)
        if availability and availability != 'all':
            qs = qs.filter(availability_status=availability)
        return qs.distinct()

class FreelancerDetailView(DetailView):
    model = CustomUser
    template_name = 'marketplace/detail.html'
    context_object_name = 'freelancer'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['portfolio'] = self.object.portfolio_items.all()[:4]
        return ctx
