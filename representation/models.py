# coding: utf-8
import os
import uuid
from django.contrib.auth.models import User
from django.db import models

genders = (
    ("m", "Male"),
    ("fm", "Female"),
)


def get_path_user_photo(instance, filename):
    ext = filename.split('.')[-1]
    path = os.path.join("users", "avatar")
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(path, str(instance.user.id), filename)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    sex = models.CharField(max_length=2, choices=genders, blank=True)
    birthday = models.DateField(null=True, blank=True)
    home_town = models.CharField(max_length=50, blank=True)
    languages = models.ManyToManyField('Language', blank=True)

    country = models.ForeignKey('Country', null=True, blank=True)
    city = models.ForeignKey('City', null=True, blank=True)
    e_mail = models.EmailField(null=True, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    additional_phone = models.CharField(max_length=100, blank=True)
    personal_site = models.CharField(max_length=255, blank=True)

    activity = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    favorite_music = models.TextField(blank=True)
    favorite_films = models.TextField(blank=True)
    favorite_books = models.TextField(blank=True)
    favorite_games = models.TextField(blank=True)

    user_photo_avatar = models.ImageField(blank=True, upload_to=get_path_user_photo)

    def __unicode__(self):
        return "%s: %s %s" % (self.user.username, self.name, self.first_name)


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey('Country')
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name
