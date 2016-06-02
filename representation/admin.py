# coding: utf-8
from django.contrib import admin

from representation.models import Language, Country, City, UserProfile, FriendRequest, Message, PostComment, Post


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'birthday']
    list_filter = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'accepted', 'denied']
    readonly_fields = list_display + ['message']
    search_fields = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user_sender', 'user_recipient', 'date', 'read']
    readonly_fields = list_display + ['text']
    search_fields = list_display
    list_filter = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'date']
    readonly_fields = list_display + ['text', 'post']
    search_fields = list_display
    list_filter = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'place', 'date']
    readonly_fields = list_display + ['text']
    search_fields = list_display
    list_filter = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
