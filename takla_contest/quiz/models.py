from django.contrib.auth.models import User
from django.db import models


# # Create your models here.
# class Comment(models.Model):
#     text = models.TextField(max_length=2048, blank=True)
#     author = models.CharField(max_length=128, blank=True)


class QuestionSet(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id)+" "+self.description


class Question(models.Model):
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    type = models.IntegerField(
        default=0,
        help_text="0: short, 1: long, 2: mcq"
    )

    def __str__(self):
        return str(self.type)+" "+self.description


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=800, null=True, blank=True)
    submission_time = models.DateTimeField(auto_now=True)
    marks = models.IntegerField(default=0)










