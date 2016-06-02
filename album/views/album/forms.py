from django.forms import ModelForm

from album.models import Album


class CreateAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_private']


class EditAlbumForm(ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_private', 'cover']
