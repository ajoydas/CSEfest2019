from django.contrib import admin

# Register your models here.
from hunt.models import Game, TeamGame, TeamTask, TeamTaskStatus, Tries


class GameAdmin(admin.ModelAdmin):
    # list_display = ('img_show',)
    fields = ('serial_no','pdf','answer','location','location_show','location_clue','endgame_key','penalty_key',)
    readonly_fields = ('location_show',)



admin.site.register(Game, GameAdmin)

models = [ TeamGame, TeamTask, TeamTaskStatus, Tries]
admin.site.register(models)