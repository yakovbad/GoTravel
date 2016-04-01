# coding: utf-8
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import FormView
from representation.models import Message
from representation.views.views import AllPageView
from .forms import SendMessage


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', MessageBasePageView.as_view(), name='base'),
        url(r'^id(?P<message_id>\d+)$', MessageShowPageView.as_view(), name='show'),
        url(r'^new/(?P<user_id>\d+)$', MessageShowPageView.as_view(), name='new')
    ]

    return include(urlpatterns, namespace='message')


class MessageBasePageView(AllPageView):
    http_method_names = ['get']
    template_name = 'representation/message/base.html'

    def get_context_data(self, **kwargs):
        context = super(MessageBasePageView, self).get_context_data(**kwargs)

        context['messages'] = self.request.user.user_recipient_message.order_by("-date")
        context['messages_out'] = self.request.user.user_sender_message.order_by("-date")

        return context


class MessageShowPageView(FormView, AllPageView):
    http_method_names = ['get', 'post']
    form_class = SendMessage
    template_name = 'representation/message/show.html'

    def get_context_data(self, **kwargs):
        context = super(MessageShowPageView, self).get_context_data(**kwargs)

        try:
            message = Message.objects.get(id=int(self.kwargs['message_id']))
            message.read = True
            message.save()
            context['message'] = message
        except Exception:
            pass

        context['form'] = self.form_class

        return context

    def form_valid(self, form):
        try:
            user_recipient = Message.objects.get(id=int(self.kwargs['message_id'])).user_sender
        except KeyError:
            user_recipient = User.objects.get(id=int(self.kwargs['user_id']))
        Message(user_sender=self.request.user,
                user_recipient=user_recipient,
                text=form.cleaned_data['text']).save()
        return super(MessageShowPageView, self).form_valid(form)

    def get_success_url(self):
        return reverse('representation:message:base')
