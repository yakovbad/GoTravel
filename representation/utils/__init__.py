from django.http import Http404, HttpResponseRedirect


def post(method):
    def wrapper(*args, **kwargs):
        if args[0].method == "POST":
            return method(*args, **kwargs)
        else:
            raise Http404
    return wrapper
