from django.contrib import admin
from .models import CustomUser, Skill, Profile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'school', 'verified', 'availability_status')
    list_filter = ('verified', 'school', 'availability_status')
    search_fields = ('full_name', 'username', 'whatsapp')
    actions = ['verify_students']

    def verify_students(self, request, queryset):
        queryset.update(verified=True)
    verify_students.short_description = "Verify selected students"

admin.site.register(Skill)
admin.site.register(Profile)
