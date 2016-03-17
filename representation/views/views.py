from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from representation.models import UserProfile


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('representation:userPage', args=(request.user.id,)))
    return render(request, 'representation/index.html')


class AllPageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(AllPageView, self).get_context_data(**kwargs)
        count = self.request.user.user_incoming_friend_requests.filter(denied=False, accepted=False).count()
        context['request_friend_count'] = count if count > 0 else ''
        return context


class UserPageView(AllPageView):
    http_method_names = ['get']
    template_name = 'representation/index.html'

    def get_context_data(self, **kwargs):
        context = super(UserPageView, self).get_context_data(**kwargs)
        user_id = int(self.kwargs['user_id'])
        context['user_outgoing_friend_requests'] = self.request.user.user_outgoing_friend_requests\
            .filter(to_user__id=user_id).filter(denied=False, accepted=False)
        if self.request.user.id == user_id:
            context['user_profile'] = UserProfile.objects.get_or_create(user=self.request.user)[0]
        elif self.request.user.is_authenticated():
            try:
                context['user_profile'] = UserProfile.objects.get(user__id=user_id)
            except ObjectDoesNotExist:
                return render(self.request, '')
        return context


def test(request):
    if request.method == 'POST':
        print request.POST
    return render(request, 'representation/test.html')
