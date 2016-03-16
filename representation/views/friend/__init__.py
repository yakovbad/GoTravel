from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from representation.models import FriendRequest
from representation.views.views import AllPageView


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', FriendBaseView.as_view(), name='base'),
        url(r'^add_request/$', request_add_friends, name='requestFriendAdd'),
        url(r'^response_to_request/$', accept_request, name='responseRequestFriend'),
    ]

    return include(urlpatterns, namespace='friend')


def request_add_friends(request):
    if request.method == 'POST':
        to_user = User.objects.get(id=int(request.POST['to_user']))
        _fr = FriendRequest.objects.filter(from_user=to_user)
        if _fr.exists():
            _fr.first().accept(to_user)
        else:
            FriendRequest(from_user=request.user, to_user=to_user).save()
            request.user.following.add(to_user.user_profile.get())
            to_user.follower.add(request.user.user_profile.get())
        return redirect(reverse('representation:userPage', args=(to_user.id,)))


def accept_request(request):
    if request.method == 'POST':
        fr = None
        try:
            fr = FriendRequest.objects.get(id=int(request.POST['request_id']))
        except KeyError:
            redirect(reverse('representation:friend:base'))
        if 'accept' in request.POST:
            fr.accept(fr.from_user)
        elif 'deny' in request.POST:
            fr.deny(fr.from_user)
    return redirect(reverse('representation:friend:base'))


class FriendBaseView(AllPageView):
    template_name = 'representation/friends.html'

    def get_context_data(self, **kwargs):
        context = super(FriendBaseView, self).get_context_data(**kwargs)
        context['request_friend'] = self.request.user.user_incoming_friend_requests.filter(denied=False, accepted=False)
        return context
