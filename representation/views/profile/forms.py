# coding: utf-8
from django.forms import ModelForm
from representation.models import UserProfile


class AddOrEditProfile(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'name',
            'first_name',
            'sex',
            'birthday',
            'home_town',
            'languages',
        ]


class AddOrEditContact(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'country',
            'city',
            'e_mail',
            'mobile_phone',
        ]


class AddOrEditPersonalInfo(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'activity',
            'interests',
            'favorite_music',
            'favorite_films',
            'favorite_books',
            'favorite_games',
        ]


class AddOrEditUserAvatarPhoto(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user_photo_avatar']
