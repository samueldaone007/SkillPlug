from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    SCHOOL_CHOICES = [
        ('unilag', 'UNILAG'), ('uniben', 'UNIBEN'), ('oau', 'OAU'),
        ('ui', 'UI'), ('futa', 'FUTA'), ('abuja', 'UNIBEN'), ('other', 'Other')
    ]
    AVAILABILITY_CHOICES = [
        ('available', 'Available'), ('busy', 'Busy'), ('unavailable', 'Unavailable')
    ]
    full_name = models.CharField(max_length=100)
    school = models.CharField(max_length=50, choices=SCHOOL_CHOICES, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    whatsapp = models.CharField(max_length=15, blank=True, null=True, help_text="Include country code, e.g., 2348012345678")
    bio = models.TextField(max_length=500, blank=True, null=True)
    verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')

    def __str__(self):
        return self.full_name or self.username

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    skills = models.ManyToManyField(Skill, blank=True)
    whatsapp_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile for {self.user.full_name}"

    def save(self, *args, **kwargs):
        if self.user.whatsapp and not self.whatsapp_link:
            self.whatsapp_link = f"https://wa.me/{self.user.whatsapp.replace('+', '')}"
        super().save(*args, **kwargs)