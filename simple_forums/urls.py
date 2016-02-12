from django.conf.urls import url

from simple_forums import views


urlpatterns = [
    url(r'^$', views.ThreadListView.as_view(), name='thread-list'),
    url(r'^(?P<pk>[0-9]+)/(?P<thread_slug>[\w-]+)/$',
        views.ThreadDetailView.as_view(),
        name='thread-detail'),
]
