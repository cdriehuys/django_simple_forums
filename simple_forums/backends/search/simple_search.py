from functools import reduce
import warnings

from django.db.models import Q

from simple_forums import models
from simple_forums.backends.search import BaseSearch


class SimpleSearch(BaseSearch):
    """ Simple ORM based search """

    def add(self, object):
        """ Not implemented in this backend """
        warnings.warn('add is not implemented in this backend')

    def remove(self, object):
        """ Not implemented in this backend """
        warnings.warn('remove is not implemented in this backend')

    def search(self, query_string):
        """ Search all thread instances for the given query string """
        return models.Thread.objects.filter(
            reduce(
                lambda q, f: q & Q(title__icontains=f),
                query_string.split(),
                Q()))
