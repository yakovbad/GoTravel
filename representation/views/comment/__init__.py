from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import FormView

from representation.models import Comment, Post
from representation.views.comment.forms import AddCommentToPostForm


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^wall(?P<user_id>\d+)/(?P<post_id>\d+)$', CommentAddToPostView.as_view(), name='addToPost'),
        url(r'^delete/(?P<comment_id>\d+)', delete_comment, name='delete'),
    ]
    return include(urlpatterns, namespace='comment')


class CommentAddToPostView(FormView):
    http_method_names = ['post']
    form_class = AddCommentToPostForm

    def form_valid(self, form):
        post = Post.objects.get(id=self.kwargs['post_id'])
        Comment(author=self.request.user, post=post, text=form.cleaned_data['text']).save()
        return super(CommentAddToPostView, self).form_valid(form)

    def get_success_url(self):
        return reverse('representation:post:all', args=(self.kwargs['user_id'],))


def delete_comment(request, comment_id):
    if request.method == 'POST':
        c = Comment.objects.get(id=comment_id)
        post = c.post
        if request.user == c.author or request.user == post.author or request.user == post.place:
            c.delete()
        return redirect(reverse('representation:post:all', args=(post.place.id,)))
