from django.contrib import admin
from core.models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'marks','submitted', 'submission_time')


admin.site.register(Profile, ProfileAdmin)
