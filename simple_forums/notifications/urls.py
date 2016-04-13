from django.conf.urls import url

from simple_forums.notifications import views


urlpatterns = [
    url(r'thread/(?P<pk>[0-9]+)/follow/$',
        views.ThreadNotificationCreate.as_view(),
        name='follow-thread')
]
