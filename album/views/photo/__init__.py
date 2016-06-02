from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import CreateView

from album.views.photo.forms import UploadPhotoForm


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', PhotoUploadView.as_view(), name='root'),
    ]

    return include(urlpatterns, namespace='photo')


class PhotoUploadView(CreateView):
    template_name = "album/upload_photo.html"
    form_class = UploadPhotoForm
    http_method_names = ['get', 'post']

    def get_success_url(self):
        return reverse('album:album:root', args=(self.request.user.id,))
