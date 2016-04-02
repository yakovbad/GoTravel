# coding: utf-8
import os
import uuid

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

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
    user = models.ForeignKey(User, related_name='user_profile')
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

    #todo переделать когда добавлю фото пользователя
    user_photo_avatar = models.ImageField(blank=True, upload_to=get_path_user_photo)

    friends = models.ManyToManyField(User, related_name='friends', blank=True)
    followers = models.ManyToManyField(User, related_name='follower', blank=True)
    followings = models.ManyToManyField(User, related_name='following', blank=True)

    def __unicode__(self):
        return "%s: %s %s" % (self.user.username, self.name, self.first_name)

    def get_full_name(self):
        return "%s %s" % (self.name, self.first_name)


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


class FriendRequest(models.Model):

    from_user = models.ForeignKey(User, related_name='user_outgoing_friend_requests', verbose_name=_(u'Requester'))
    to_user = models.ForeignKey(User, related_name='user_incoming_friend_requests', verbose_name=_(u'Receiver'))
    message = models.TextField(null=True, blank=True, verbose_name=_(u'Message'))
    accepted = models.BooleanField(default=False, verbose_name=_(u'Accepted'))
    denied = models.BooleanField(default=False, verbose_name=_(u'Denied'))

    def __unicode__(self):
        return "[%s]%s wants to make friends %s" % (self.id, self.from_user, self.to_user)

    def accept(self, by_user):
        if by_user == self.to_user:
            return False
        self.to_user.user_profile.get().friends.add(by_user)
        self.to_user.user_profile.get().followers.remove(by_user)
        by_user.user_profile.get().friends.add(self.to_user)
        by_user.user_profile.get().followings.remove(self.to_user)
        self.accepted = True
        self.save()
        return True

    def deny(self, by_user):
        if by_user == self.to_user or self.denied or self.accepted:
            return False
        self.denied = True
        self.save()


class Message(models.Model):

    user_sender = models.ForeignKey(User, related_name='user_sender_message')
    user_recipient = models.ForeignKey(User, related_name='user_recipient_message')
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now())
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s to %s date=%s" % (self.user_sender, self.user_recipient, self.date)


class PostComment(models.Model):
    author = models.ForeignKey(User, related_name="author_comment")
    date = models.DateTimeField(default=datetime.now())
    text = models.TextField()
    post = models.ForeignKey('Post', related_name="comment_post", blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.text[:50])


class Post(models.Model):

    author = models.ForeignKey(User, related_name='author_post')
    place = models.ForeignKey(User, related_name='place_post')
    date = models.DateTimeField(default=datetime.now())
    text = models.TextField()

    def __unicode__(self):
        return "%s" % (self.text[:50])
