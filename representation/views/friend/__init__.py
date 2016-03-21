from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from representation.models import FriendRequest, UserProfile
from representation.views.views import AllPageView


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', FriendBaseView.as_view(), name='base'),
        url(r'^add_request/$', request_add_friends, name='requestFriendAdd'),
        url(r'^delete/$', delete_friend, name='FriendDelete'),
        url(r'^response_to_request/$', accept_request, name='responseRequestFriend'),
    ]

    return include(urlpatterns, namespace='friend')


class FriendBaseView(AllPageView):
    template_name = 'representation/friends.html'

    def get_context_data(self, **kwargs):
        context = super(FriendBaseView, self).get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        context['request_friend'] = self.request.user.user_incoming_friend_requests.filter(denied=False, accepted=False)
        return context


def request_add_friends(request):
    if request.method == 'POST':
        to_user = User.objects.get(id=int(request.POST['to_user']))
        _fr = FriendRequest.objects.filter(from_user=to_user, accepted=False)
        if _fr.exists():
            _fr.first().accept(to_user)
        else:
            FriendRequest(from_user=request.user, to_user=to_user).save()
            request.user.user_profile.get().followings.add(to_user)
            to_user.user_profile.get().followers.add(request.user)
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


def delete_friend(request):
    to_user = None
    if request.method == 'POST':
        to_user = User.objects.get(id=int(request.POST['to_user']))
        fr = FriendRequest.objects.filter(to_user=to_user, from_user=request.user)
        if not fr.first():
            fr = FriendRequest.objects.filter(to_user=request.user, from_user=to_user)
        fr = fr.first()
        print fr
        fr.from_user.user_profile.get().friends.remove(fr.to_user)
        fr.to_user.user_profile.get().friends.remove(fr.from_user)
        if request.user == fr.to_user:
            to_user.user_profile.get().followings.add(request.user)
            request.user.user_profile.get().followers.add(to_user)
    return redirect(reverse('representation:userPage', args=(to_user.id,)))
