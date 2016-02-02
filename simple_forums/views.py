from django.views import generic

from simple_forums import models


class ThreadDetailView(generic.DetailView):
    """ View for getting a thread's details """

    model = models.Thread


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread
