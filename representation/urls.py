
from django.conf.urls import url

from representation.views import auth, views, profile

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^id(?P<user_id>\d+)', views.user_page, name='userPage'),
    url(r'^profile/', profile.url_view()),
    url(r'^auth/', auth.url_view()),
]
