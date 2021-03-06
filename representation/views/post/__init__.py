from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from representation.models import Post
from representation.views.comment import AddCommentToPostForm
from representation.views.post.forms import AddPostForm
from representation.views.views import AllPageView


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^$', PostBasePageView.as_view(), name='all'),
        url(r'^add/', PostAddView.as_view(), name='add'),
        url(r'^delete/(?P<post_id>\d+)', delete_post, name='delete'),
    ]
    return include(urlpatterns, namespace='post')


class PostBasePageView(AllPageView):
    http_method_names = ['get']
    template_name = 'representation/post/index.html'

    def get_context_data(self, **kwargs):
        context = super(PostBasePageView, self).get_context_data(**kwargs)

        context['form'] = AddPostForm
        context['user_id'] = self.kwargs['user_id']

        context['form_comment'] = AddCommentToPostForm

        posts = Post.objects.filter(place__id=context['user_id'])
        comments = {}
        for item in posts:
            comments[item] = item.comment_post.order_by('-date')
        context['post_with_comments'] = comments
        return context


class PostAddView(FormView):
    form_class = AddPostForm
    http_method_names = ['post']

    def form_valid(self, form):
        place = User.objects.get(id=self.kwargs['user_id'])
        author = self.request.user
        Post(author=author, place=place, text=form.cleaned_data['text']).save()
        return super(PostAddView, self).form_valid(form)

    def get_success_url(self):
        return reverse('representation:post:all', args=(self.kwargs['user_id'],))


def delete_post(request, user_id, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        if request.user == post.author or request.user == post.place:
            post.delete()
        return redirect(reverse('representation:post:all', args=(user_id,)))
