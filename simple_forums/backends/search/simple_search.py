from functools import reduce

from django.db.models import Q

from simple_forums import models


class SimpleSearch(object):
    """ Simple ORM based search """

    def search(self, query_string):
        """ Search all thread instances for the given query string """
        return models.Thread.objects.filter(
            reduce(
                lambda q, f: q & Q(title__icontains=f),
                query_string.split(),
                Q()))
