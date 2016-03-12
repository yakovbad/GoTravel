# coding: utf-8
from django.shortcuts import render
from .forms import AddOrEditProfile, AddOrEditContact, AddOrEditPersonalInfo, AddOrEditUserAvatarPhoto
from representation.models import UserProfile


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^base/$', base, name='base'),
        url(r'^contact/$', contact, name='contact'),
        url(r'^userinfo/$', user_personal_info, name='userinfo'),
        url(r'^photo/$', user_photo_upload, name='photo'),
    ]

    return include(urlpatterns, namespace='profile')


def base(request):
    context = dict()
    if request.method == 'GET':
        context['form'] = AddOrEditProfile(instance=UserProfile.objects.get_or_create(user=request.user)[0])
    elif request.method == 'POST':
        f = AddOrEditProfile(request.POST, instance=UserProfile.objects.get(user=request.user))
        if f.is_valid():
            _instance = f.save(commit=False)
            _instance.user = request.user
            _instance.save()
            f.save_m2m()
            context['form'] = AddOrEditProfile(instance=_instance)
        else:
            context['form'] = f
    return render(request, 'representation/profile_base.html', context)


def contact(request):
    context = dict()
    if request.method == 'GET':
        context['form'] = AddOrEditContact(instance=UserProfile.objects.get_or_create(user=request.user)[0])

    return render(request, 'representation/profile_contact.html', context)


def user_personal_info(request):
    context = dict()
    if request.method == 'GET':
        context['form'] = AddOrEditPersonalInfo(instance=UserProfile.objects.get_or_create(user=request.user)[0])
    return render(request, 'representation/profile_contact.html', context)


def user_photo_upload(request):
    context = dict()
    if request.method == 'GET':
        context['form'] = AddOrEditUserAvatarPhoto(instance=UserProfile.objects.get_or_create(user=request.user)[0])
    return render(request, 'representation/profile_contact.html', context)
