from django.conf.urls import url

from simple_forums import views


urlpatterns = [
    url(r'^$', views.ThreadListView.as_view(), name='thread-list'),
]
