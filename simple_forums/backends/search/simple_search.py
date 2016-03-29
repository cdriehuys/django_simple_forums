from functools import reduce

from django.db.models import Q

from simple_forums import models
from simple_forums.backends.search import BaseSearch, SearchResultSet


class SimpleSearch(BaseSearch):
    """ Simple ORM based search """

    def add(self, object):
        """ Not implemented in this backend """

    def remove(self, object):
        """ Not implemented in this backend """

    def search(self, query_string):
        """ Search all thread instances for the given query string """
        threads = models.Thread.objects.filter(
            reduce(
                lambda q, f: q & Q(title__icontains=f),
                query_string.split(),
                Q()))

        result_set = SearchResultSet()
        for thread in threads:
            result_set.add(thread)

        return result_set

    def wipe(self):
        """ Not implemented in this backend """
