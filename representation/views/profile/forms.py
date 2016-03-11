# coding: utf-8
from django.forms import ModelForm
from representation.models import UserProfile, Contact


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
        model = Contact
        fields = [
            'country',
            'city',
            'e_mail',
            'mobile_phone',
        ]
