# coding: utf-8
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
    ]

    return include(urlpatterns, namespace='message')


class MessageBasePageView(AllPageView):
    http_method_names = ['get']
    template_name = 'representation/message/base.html'

    def get_context_data(self, **kwargs):
        context = super(MessageBasePageView, self).get_context_data(**kwargs)

        context['messages'] = self.request.user.user_recipient_message.all()
        context['messages_out'] = self.request.user.user_sender_message.all()

        return context


class MessageShowPageView(FormView, AllPageView):
    http_method_names = ['get', 'post']
    form_class = SendMessage
    template_name = 'representation/message/show.html'

    def get_context_data(self, **kwargs):
        context = super(MessageShowPageView, self).get_context_data(**kwargs)

        message = Message.objects.get(id=int(self.kwargs['message_id']))
        message.read = True
        message.save()
        context['message'] = message

        context['form'] = self.form_class

        return context

    def form_valid(self, form):
        #todo added message to database
        return super(MessageShowPageView, self).form_valid(form)

    def get_success_url(self):
        return reverse('representation:message:show', args=(self.kwargs['message_id'],))
