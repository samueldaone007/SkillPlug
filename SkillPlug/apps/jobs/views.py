from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Job, Application

class JobListView(ListView):
    model = Job
    template_name = 'jobs/list.html'
    context_object_name = 'jobs'
    ordering = ['-created_at']
    paginate_by = 10

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['applications_count'] = self.object.applications.count()
        return ctx

class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['title', 'description', 'budget']
    template_name = 'jobs/post_job.html'
    success_url = reverse_lazy('jobs_list')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, 'Job posted successfully!')
        return super().form_valid(form)

class JobApplyView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['message']
    template_name = 'jobs/apply.html'

    def form_valid(self, form):
        form.instance.job_id = self.kwargs['pk']
        form.instance.student = self.request.user
        try:
            messages.success(self.request, 'Application sent!')
            return super().form_valid(form)
        except Exception:
            messages.error(self.request, 'You already applied to this job.')
            from django.shortcuts import redirect
            return redirect('job_detail', pk=self.kwargs['pk'])

    def get_success_url(self):
        return reverse_lazy('job_detail', kwargs={'pk': self.object.job_id})
