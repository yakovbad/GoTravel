
from django.conf.urls import url
from representation.views import auth, views, profile, friend, message, post, comment

urlpatterns = [
    url(r'^test/', views.test, name='test'),

    url(r'^$', views.index, name='index'),
    url(r'^id(?P<user_id>\d+)', views.UserPageView.as_view(), name='userPage'),
    url(r'^auth/', auth.url_view()),

    url(r'^profile/', profile.url_view()),
    url(r'^friends/', friend.url_view()),
    url(r'^message/', message.url_view()),
    url(r'^wall(?P<user_id>\d+)/', post.url_view()),
    url(r'^comment/', comment.url_view()),
]
