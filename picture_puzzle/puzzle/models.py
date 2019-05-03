"""
######################### Documentation Begin #########################
======================================================================
---------------
@models.CASCADE
---------------
A foreign key with cascade delete means that if a record in the parent
table is deleted, then the corresponding records in the child table
will automatically be deleted. This is called a cascade delete in SQL.

Django emulates the behavior of the SQL constraint ON DELETE CASCADE
and also deletes the object containing the ForeignKey.


----------------
@models.SET_NULL
----------------
Django Set the ForeignKey null; this is only possible if null is True.
======================================================================
######################### Documentation End   #########################
"""
import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


# Create your models here.'
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.deconstruct import deconstructible
from django.utils.safestring import mark_safe

from picture_puzzle.settings import MEDIA_ROOT


class Tag(models.Model):
    name = models.CharField(null=False, max_length=100)

    class Meta:
        verbose_name_plural = "Tag"

    def __str__(self):
        return self.name


# @deconstructible
# class UploadToPathAndRename(object):
#     def __init__(self, path):
#         self.sub_path = path
#
#     def __call__(self, instance, filename):
#         ext = filename.split('.')[-1]
#         # get filename
#         if instance.pk:
#             filename = '{}.{}'.format(instance.pk, ext)
#         else:
#             # set filename as random string
#             filename = '{}.{}'.format(uuid4().hex, ext)
#         # return the whole path to the file
#         return os.path.join(self.sub_path, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'pictures/{0}'.format(filename)

class Puzzle(models.Model):
    # serial_no = models.IntegerField(unique=True, null=False)
    # type = models.IntegerField(null=False)
    id = models.IntegerField(primary_key=True)
    info = models.CharField(null=True, blank=True, max_length=300)
    info_link = models.URLField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    fact = models.CharField(null=True, blank=True, max_length=300)
    image = models.FileField(upload_to=user_directory_path, null=True)
    tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL, related_name='tag')
    ans = models.CharField(null=False, max_length=200)
    visible = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Puzzle"

    def __str__(self):
        return self.ans

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def img_show(self):  # receives the instance as an argument
        return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
            thumb=self.image.url,
        ))

    img_show.allow_tags = True
    img_show.short_description = 'Current Puzzle'

# class Image(models.Model):
#     img = models.FileField(upload_to='pictures', blank=True)
#
#     class Meta:
#         verbose_name_plural = "Image"
#
#     def get_picture(self):
#         if self.img and hasattr(self.img, 'url'):
#             return self.img.url
#         return None
#
#     def img_show(self):  # receives the instance as an argument
#         return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
#             thumb=self.img.url,
#         ))
#
#     img_show.allow_tags = True
#     img_show.short_description = 'Current Image'



# class Type1(models.Model):
#     puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='type_1_puzzle')
#
#
#     class Meta:
#         verbose_name_plural = "Type_1_Image"
#
#     def __str__(self):
#         return self.ans


# class Type2(models.Model):
#     puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='type_2_puzzle')
#     img1 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_2_image_1')
#     img2 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_2_image_2')
#     img3 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_2_image_3')
#     img4 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_2_image_4')
#     tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name='type_2_tag', null=True)
#     ans = models.CharField(null=False, max_length=200)
#
#     class Meta:
#         verbose_name_plural = "Type_2_Image"
#
#
# class Type3(models.Model):
#     puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, related_name='type_3_puzzle')
#     img1 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_3_image_1')
#     img2 = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='type_3_image_2')
#     tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, related_name='type_3_tag', null=True)
#     ans = models.CharField(null=False, max_length=200)
#
#     class Meta:
#         verbose_name_plural = "Type_3_Image"
#

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    tried = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    showed_meme = models.BooleanField(default=False)


def meme_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return 'memes/{0}'.format(filename)

class Meme(models.Model):
    image = models.FileField(upload_to=meme_directory_path, blank=True)
    sound = models.FileField(upload_to=meme_directory_path, blank=True)
    text = models.CharField(null=True, max_length=300)
    # For Students or Alumn
    account_type = models.IntegerField(default=-1, help_text="Alum = 0 & Student = 1")
    # For success or fail
    type = models.IntegerField(default=-1, help_text="Fail = 0 & Success = 1")

    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return None

    def img_show(self):  # receives the instance as an argument
        return mark_safe('<img src="{thumb}" width="200" height="150" />'.format(
            thumb=self.image.url,
        ))

    img_show.allow_tags = True
    img_show.short_description = 'Current Meme'

    def music_play(self):  # receives the instance as an argument
        try:
            return mark_safe('<audio tabindex="0" controls><source src="{music}"></audio>'.format(
                music=self.sound.url,
            ))
        except:
            return ('No Sound')

    music_play.allow_tags = True
    music_play.short_description = 'Current Sound'

    class Meta:
        verbose_name_plural = "Meme"


class Music(models.Model):
    music = models.FileField(upload_to='musics')

    def music_play(self):  # receives the instance as an argument
        return mark_safe('<audio tabindex="0" controls><source src="{music}"></audio>'.format(
            music=self.music.url,
        ))

    music_play.allow_tags = True
    music_play.short_description = 'Current Music'


class Submitted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

