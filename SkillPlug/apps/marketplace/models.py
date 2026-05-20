from django.db import models
from apps.accounts.models import CustomUser

class PortfolioItem(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio_items')
    image = models.ImageField(upload_to='portfolio/')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title