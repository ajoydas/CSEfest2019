from django.contrib import admin

# Register your models here.
# from .models import Comment
#
# admin.site.register(Comment)
from quiz.models import Question, QuestionSet, Submission


class QuestionSetAdmin(admin.ModelAdmin):
    list_display = ("id", "description")


admin.site.register(QuestionSet, QuestionSetAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id","question_set", "type", "description")


admin.site.register(Question, QuestionAdmin)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "question", "answer", "submission_time")


admin.site.register(Submission, SubmissionAdmin)
