from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level_completed = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True)
    start_code = models.CharField(max_length=6)
    password = models.CharField(max_length=20,null=True)

    class Meta:
        db_table = 'user_profile'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
