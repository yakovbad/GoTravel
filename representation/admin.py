# coding: utf-8
from django.contrib import admin

from representation.models import Language, Country, City, UserProfile, FriendRequest, Message, Comment, Post

admin.site.register(Language)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(UserProfile)
admin.site.register(FriendRequest)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Post)
