from django.conf.urls import url

from album.views import album, photo

urlpatterns = [
    url(r'^user(?P<user_id>\d+)/', album.url_view()),
    url(r'^user(?P<user_id>\d+)/upload/', photo.url_view())
]