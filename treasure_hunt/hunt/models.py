from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe

from core.views import gen_key


# class Game(models.Model):
#     serial_no = models.IntegerField(unique=True, blank=False)
#     pdf = models.FileField(upload_to='puzzle', null=True)
#     answer = models.CharField(max_length=100)
#     location_clue = models.FileField(upload_to='location', null=True)
#     location = models.CharField(max_length=200)
#     startgame_key = models.CharField(max_length=6, null=True, blank=True)
#     endgame_key = models.CharField(max_length=6, null=True, blank=True)
#     penalty_key = models.CharField(max_length=6, null=True, blank=True)
#
#     def location_show(self):  # receives the instance as an argument
#         return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
#             thumb=self.location_clue.url,
#         ))
#
#     location_show.allow_tags = True
#     location_show.short_description = 'Location Image'
#
#     def save(self, *args, **kwargs):
#         if not self.startgame_key :
#             self.startgame_key = None
#
#         if not self.endgame_key:
#             self.endgame_key = None
#
#         if not self.penalty_key:
#             self.penalty_key = None
#
#         super(Game, self).save(*args, **kwargs)

class Game(models.Model):
    serial_no = models.IntegerField(unique=True, blank=False)
    pdf = models.FileField(upload_to='puzzle', null=True)
    answer = models.CharField(max_length=100)
    location_clue = models.FileField(upload_to='location', null=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    # startgame_key = models.CharField(max_length=6, null=True, blank=True)
    endgame_key = models.CharField(max_length=6, null=True, blank=True)
    penalty_key = models.CharField(max_length=6, null=True, blank=True)

    def location_show(self):  # receives the instance as an argument
        return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
            thumb=self.location_clue.url,
        ))

    location_show.allow_tags = True
    location_show.short_description = 'Location Image'

    def save(self, *args, **kwargs):
        # if not self.startgame_key :
        #     self.startgame_key = None

        if not self.endgame_key:
            self.endgame_key = None

        if not self.penalty_key:
            self.penalty_key = None

        super(Game, self).save(*args, **kwargs)

class TeamGame(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    # startgame_time = models.DateTimeField(null=True)
    endgame_time = models.DateTimeField(null=True)
    puzzle_get_time = models.DateTimeField(null=True)
    puzzle_sub_time = models.DateTimeField(null=True)
    puzzle_tried = models.IntegerField(default=0)
    puzzle_finished = models.BooleanField(default=False)
    game_finished = models.BooleanField(default=False)
    game_finished_time = models.DateTimeField(null=True)


class TeamTask(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    tasks = models.CharField(max_length=50, blank=False)


class TeamTaskStatus(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Game, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, default='n')


class Tries(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Game, on_delete=models.CASCADE)
    text = models.CharField(max_length=50, blank=True, null=True)


@receiver(pre_save, sender=Game)
def add_game_keys(sender, instance, **kwargs):
    # start = instance.startgame_key
    end = instance.endgame_key
    penalty = instance.penalty_key

    # if start is None or start == '':
    #     instance.startgame_key = gen_key()

    if end is None or end == '':
        instance.endgame_key = gen_key()

    if penalty is None or penalty == '':
        instance.penalty_key = gen_key()


@receiver(post_save, sender=TeamTask)
def add_team_task_status(sender, instance, created, **kwargs):
    if not created:
        TeamTaskStatus.objects.filter(team=instance.team).delete()

    task_list = instance.tasks
    tasks = list(map(int, task_list.split(',')))
    print(tasks)
    for task in tasks:
        game = Game.objects.filter(serial_no=task).get()
        status = TeamTaskStatus()
        status.team = instance.team
        status.task = game
        status.save()
