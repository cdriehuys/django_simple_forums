from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

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

    url(r'^login/$', auth_views.login,
        {'template_name': 'simple_forums/login.html'},
        name='login'),

    url(r'^logout/$', auth_views.logout,
        {
            'next_page': reverse_lazy('topic-list'),
        },
        name='logout'),

    url(r'^new/$', views.ThreadCreateView.as_view(), name='thread-create')
]
