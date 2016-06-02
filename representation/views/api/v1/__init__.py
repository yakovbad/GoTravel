from representation.views.api.v1 import wall


def url_view():
    from django.conf.urls import url, include

    urlpatterns = [
        url(r'^wall/(?P<wall_id>\d+)/', wall.url_view()),
    ]
    return include(urlpatterns, namespace='api_v1')