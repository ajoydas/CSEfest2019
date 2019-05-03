from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Puzzle, Tag, Meme, Submission, Music, Submitted


class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('id','img_show','tag', 'ans', 'visible')
    fields = ('id', 'visible', 'img_show', 'image',  'ans', 'tag',
              'info', 'info_link', 'title', 'fact',)
    readonly_fields = ('img_show',)


admin.site.register(Puzzle, PuzzleAdmin)


class MemeAdmin(admin.ModelAdmin):
    list_display = ('img_show', 'music_play')
    fields = ('img_show','image', 'music_play', 'sound', 'text', 'account_type', 'type')
    readonly_fields = ('img_show','music_play')


admin.site.register(Meme, MemeAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'puzzle', 'tried', 'accepted', 'showed_meme', 'updated_at')


admin.site.register(Submission, SubmissionAdmin)


class SubmittedAdmin(admin.ModelAdmin):
    list_display = ('user', 'puzzle', 'text')


admin.site.register(Submitted, SubmittedAdmin)


class MusicAdmin(admin.ModelAdmin):
    list_display = ('id', 'music_play',)
    fields = ('music_play','music')
    readonly_fields = ('music_play',)


admin.site.register(Music, MusicAdmin)

# Register your models here.
models = [Tag]
admin.site.register(models)
