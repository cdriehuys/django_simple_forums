from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('simple_forums.urls')),
]
