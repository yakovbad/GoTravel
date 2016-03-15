from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from representation.models import UserProfile


def index(request):
    if request.user.is_authenticated():
        return redirect(reverse('representation:userPage', args=(request.user.id,)))
    return render(request, 'representation/index.html')


def user_page(request, user_id):
    context = dict()
    user_id = int(user_id)
    if request.user.id == user_id:
        context['user_profile'] = UserProfile.objects.get_or_create(user=request.user)[0]
    elif request.user.is_authenticated():
        try:
            context['user_profile'] = UserProfile.objects.get(user__id=user_id)
        except ObjectDoesNotExist:
            return render(request, '')

    return render(request, 'representation/index.html', context)

