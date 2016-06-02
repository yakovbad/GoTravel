from django.contrib.auth.models import User
from django.core import serializers
from django.http import HttpResponse

from representation.models import Post
from representation.views.post import AddPostForm


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$',root, name='root'),
        url(r'^add/$', add, name='add'),
        url(r'^comment/$', add_comment, name='add_comment')
    ]
    return include(urlpatterns, namespace='wall')


def root(request, wall_id):
    response = {}
    if request.method == "GET":
        if request.is_ajax():
            p = Post.objects.filter(place__id=wall_id).order_by('-date')
            response = serializers.serialize('json', p, use_natural_foreign_keys=True)
    return HttpResponse(response, content_type='application/json')


def add(request, wall_id):
    response = {}
    if request.method == "POST":
        if request.is_ajax():
            f = AddPostForm(request.POST)
            if f.is_valid():
                Post(author=request.user.user_profile, place=User.objects.get(id=wall_id).user_profile, text=f.cleaned_data['text']).save()
                response = serializers.serialize('json', [Post.objects.last(), ], use_natural_foreign_keys=True)
    return HttpResponse(response, content_type='application/json')


def add_comment(request, wall_id):
    response = ""
    return HttpResponse(response, content_type='application/json')
