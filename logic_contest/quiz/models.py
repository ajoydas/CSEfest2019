from django.contrib.auth.models import User
from django.db import models


# # Create your models here.
# class Comment(models.Model):
#     text = models.TextField(max_length=2048, blank=True)
#     author = models.CharField(max_length=128, blank=True)
from django.utils.safestring import mark_safe


class QuestionSet(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)+" "+self.description


class Question(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    # image = models.FileField(upload_to="puzzle", blank=True)
    #
    # def get_image(self):
    #     if self.image and hasattr(self.image, 'url'):
    #         return self.image.url
    #     return None
    #
    # def img_show(self):  # receives the instance as an argument
    #     return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
    #         thumb=self.image.url,
    #     ))
    #
    # img_show.allow_tags = True
    # img_show.short_description = 'Current Picture'
    type = models.IntegerField(
        default=0,
        help_text="0: short, 1: long, 2: mcq"
    )

    def __str__(self):
        return str(self.type)+" "+self.description


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    submission_time = models.DateTimeField(auto_now=True)
    marks = models.IntegerField(default=0)










