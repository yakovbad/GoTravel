from django.shortcuts import render

from representation.models import UserProfile


def index(request):
    context = dict()
    if request.user.is_authenticated():
        context['user_profile'] = UserProfile.objects.get_or_create(user=request.user)[0]
    return render(request, 'representation/index.html', context)

