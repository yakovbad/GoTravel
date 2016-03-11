# coding: utf-8
from django.contrib import admin

from representation.models import Language, Country, City, UserProfile

admin.site.register(Language)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(UserProfile)
