# coding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import UpdateView
from .forms import AddOrEditProfile, AddOrEditContact, AddOrEditPersonalInfo, AddOrEditUserAvatarPhoto
from representation.models import UserProfile


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^base/$', ProfileFormView.as_view(), name='base'),
        url(r'^contact/$', ContactFormView.as_view(), name='contact'),
        url(r'^personal_info/$', UserPersonalFormView.as_view(), name='userinfo'),
        url(r'^photo/$', UserPhotoFormView.as_view(), name='photo'),
    ]

    return include(urlpatterns, namespace='profile')


class BaseProfileFormView(UpdateView):
    model = UserProfile
    template_name = 'representation/profile_base.html'

    def get_object(self, queryset=None):
        return self.model.objects.get_or_create(user=self.request.user)[0]


class ProfileFormView(BaseProfileFormView):
    form_class = AddOrEditProfile
    success_url = reverse_lazy('representation:profile:base')


class ContactFormView(BaseProfileFormView):
    form_class = AddOrEditContact
    template_name = 'representation/profile_contact.html'
    success_url = reverse_lazy('representation:profile:contact')


class UserPersonalFormView(BaseProfileFormView):
    form_class = AddOrEditPersonalInfo
    success_url = reverse_lazy('representation:profile:userinfo')


class UserPhotoFormView(BaseProfileFormView):
    form_class = AddOrEditUserAvatarPhoto
    template_name = 'representation/profile_photo.html'
    success_url = reverse_lazy('representation:profile:photo')

