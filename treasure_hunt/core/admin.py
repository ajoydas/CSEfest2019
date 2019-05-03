from django.contrib import admin

# Register your models here.
from core.models import Profile

models = [Profile]
admin.site.register(models)
