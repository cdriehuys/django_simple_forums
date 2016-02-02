from django.views import generic

from simple_forums import models


class ThreadListView(generic.ListView):
    """ View for listing threads """

    model = models.Thread
