from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_path_user_album(instance, filename):
    import os
    import uuid

    ext = filename.split('.')[-1]
    path = os.path.join("users", str(instance.album.owner.id), "albums", instance.album.name)
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(path, filename)


class Album(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    is_private = models.BooleanField(default=False)
    create_date = models.DateTimeField(default=timezone.now)
    cover = models.ForeignKey('Photo', related_name='cover', null=True, blank=True)

    def __unicode__(self):
        return "[%s] - %s" % (self.pk, self.name)


class Photo(models.Model):
    img = models.ImageField(upload_to=get_path_user_album)
    album = models.ForeignKey(Album, null=True, blank=True)
    description = models.TextField(blank=True)
    upload_date = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return "[%s] - %s" % (self.pk, self.img.name)


class PhotoComment(models.Model):
    photo = models.ForeignKey(Photo)
    author = models.ForeignKey(User)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
