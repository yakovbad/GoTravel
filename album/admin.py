from django.contrib import admin

from album.models import Photo, Album


@admin.register(Photo)
class AdminPhoto(admin.ModelAdmin):
    pass


@admin.register(Album)
class AdminAlbum(admin.ModelAdmin):
    pass
