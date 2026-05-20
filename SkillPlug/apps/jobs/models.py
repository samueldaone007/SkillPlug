from django.db import models
from apps.accounts.models import CustomUser

class Job(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    budget = models.CharField(max_length=50, help_text="e.g., ₦5,000 or Negotiable")
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_applications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'student')

    def __str__(self):
        return f"{self.student.full_name} -> {self.job.title}"