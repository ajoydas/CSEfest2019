from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


# class Control(models.Model):
#     show_meme = models.BooleanField(default=True)
#     show_info = models.BooleanField(default=True)
#     show_fun_fact = models.BooleanField(default=True)
#     add_music = models.BooleanField(default=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_type = models.IntegerField(default=-1)
    # booster = models.IntegerField(default=0)
    level_completed = models.IntegerField(default=0)
    meme_count = models.IntegerField(default=0)
    last_sub = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'user_profile'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


