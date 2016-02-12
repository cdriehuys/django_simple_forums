from django.views import generic

from simple_forums import models


class ThreadDetailView(generic.DetailView):
    """ View for getting a thread's details """

    model = models.Thread
    pk_url_kwarg = 'thread_pk'


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread
