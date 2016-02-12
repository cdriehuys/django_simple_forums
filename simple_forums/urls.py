from django.conf.urls import url

from simple_forums import views


urlpatterns = [
    url(r'^$', views.TopicListView.as_view(), name='topic-list'),
    url(r'^(?P<topic_pk>[0-9]+)/(?P<topic_slug>[\w-]+)/$',
        views.ThreadListView.as_view(),
        name='thread-list'),
    url((r'^(?P<topic_pk>[0-9]+)/(?P<topic_slug>[\w-]+)/'
        r'(?P<thread_pk>[0-9]+)/(?P<thread_slug>[\w-]+)/$'),
        views.ThreadDetailView.as_view(),
        name='thread-detail'),
]
