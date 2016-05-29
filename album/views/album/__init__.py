from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, FormView, UpdateView

from album.models import Album
from album.views.album.forms import CreateAlbumForm, EditAlbumForm


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', AlbumBaseView.as_view(), name='root'),
        url(r'^create/$', AlbumCreateView.as_view(), name='create'),
        url(r'^id(?P<album_id>\d+)/edit/$', AlbumEditView.as_view(), name='edit'),
        url(r'^id(?P<album_id>\d+)/$', AlbumView.as_view(), name='all_photos_in_album'),
    ]

    return include(urlpatterns, namespace='album')


class AlbumBaseView(TemplateView):
    template_name = "album/all_albums.html"
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super(AlbumBaseView, self).get_context_data(**kwargs)
        if self.request.user.id == int(kwargs['user_id']):
            context['albums'] = Album.objects.filter(owner__id=kwargs['user_id'])
        else:
            context['albums'] = Album.objects.filter(owner__id=kwargs['user_id'], is_private=False)
        return context


class AlbumView(TemplateView):
    template_name = "album/album.html"
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super(AlbumView, self).get_context_data(**kwargs)
        context['photos'] = Album.objects.get(id=kwargs['album_id']).photo_set.all()
        return context


class AlbumCreateView(FormView):
    template_name = "album/create_album.html"
    form_class = CreateAlbumForm
    http_method_names = ['get', 'post']

    def form_valid(self, form):
        Album(name=form.cleaned_data['name'], owner=self.request.user, is_private=form.cleaned_data['is_private']).save()
        return super(AlbumCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('album:album:root', args=(self.request.user.id, ))


class AlbumEditView(UpdateView):
    template_name = "album/edit_album.html"
    form_class = EditAlbumForm
    http_method_names = ['get', 'post']
    model = Album

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['album_id'])

    def get(self, request, *args, **kwargs):
        if request.user != self.get_object().owner:
            raise PermissionDenied
        return super(AlbumEditView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('album:album:root', args=(self.request.user.id, ))

# todo delete album
