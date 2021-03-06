from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from representation.models import UserProfile, Post


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('representation:userPage', args=(request.user.id,)))
    return render(request, 'representation/index.html')


class AllPageView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super(AllPageView, self).get_context_data(**kwargs)

        friend_count = self.request.user.user_incoming_friend_requests.filter(denied=False, accepted=False).count()
        context['request_friend_count'] = friend_count if friend_count > 0 else ''

        message_count = self.request.user.user_recipient_message.filter(read=False).count()
        context['not_read_message_count'] = message_count if message_count > 0 else ''
        return context


class UserPageView(AllPageView):
    http_method_names = ['get']
    template_name = 'representation/index.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_authenticated():
            raise PermissionDenied
        context = super(UserPageView, self).get_context_data(**kwargs)
        user_id = int(self.kwargs['user_id'])

        if self.request.user.id == user_id:
            context['user_profile'] = UserProfile.objects.get_or_create(user=self.request.user)[0]
        elif self.request.user.is_authenticated():
            try:
                context['user_profile'] = UserProfile.objects.get(user__id=user_id)
            except ObjectDoesNotExist:
                raise PermissionDenied

        context['user_outgoing_friend_requests'] = self.request.user.user_outgoing_friend_requests\
            .filter(to_user__id=user_id).filter(denied=False, accepted=False)
        context['user_friend'] = self.request.user.friends.filter(user__id=user_id)
        context['user_followings'] = self.request.user.user_profile.followings.filter(id=user_id)

        return context


def test(request):
    return render(request, 'representation/test.html')
