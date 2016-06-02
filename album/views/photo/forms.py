from django.forms import ModelForm

from album.models import Photo


class UploadPhotoForm(ModelForm):
    class Meta:
        model = Photo
        fields = ['album', 'description', 'img']