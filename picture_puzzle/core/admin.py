from django.contrib import admin

# Register your models here.
from core.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type','level_completed', 'meme_count', 'last_sub')


admin.site.register(Profile, ProfileAdmin)


# models = [ Profile]
# admin.site.register(models)

