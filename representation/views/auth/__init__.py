from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import redirect

from representation.utils import post
from representation.views.auth.forms import MyUserCreationForm


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^login/$', _login, name='login'),
        url(r'^logout/$', _logout, name='logout'),
        url(r'^register/$', _register, name='register'),
    ]

    return include(urlpatterns, namespace='auth')


@post
def _login(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is None:
        _user = User.objects.get(email=username)
        if _user is not None:
            user = authenticate(username=_user.username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)

    return redirect(reverse("representation:index"))


def _logout(request):
    logout(request)
    return redirect(reverse("representation:index"))


@post
def _register(request):
    form = MyUserCreationForm(request.POST)
    try:
        form.save()
        _login(request)
        return redirect(reverse("representation:index"))
    except IntegrityError as e:
        print(e.message)
    except ValueError as e:
        print(e.message)

    return redirect(reverse("representation:index"))
