from simple_forums.utils import get_setting, string_to_class


def get_search_class():
    """ Get the search backend class """
    backend_info = get_setting('search_backend', {})

    return string_to_class(
        backend_info.get(
            'search_class',
            'simple_forums.backends.search.SimpleSearch'))


class SearchResultSet:
    """ Contains objects that are the results of a search """

    def __init__(self):
        """ Create blank list of results """
        self.results = []

    def __getitem__(self, key):
        return self.results[key]

    def __iter__(self):
        """ Iterate over results """
        return iter(self.results)

    def add(self, obj, score=0):
        """ Add the given object to the result set """
        self.results.append((obj, score))

    def get_sorted(self):
        """ Get the result set ordered by score, descending """
        return sorted(self.results, key=lambda item: item[1], reverse=True)


# Make module classes easily accessible
from simple_forums.backends.search.base_search import BaseSearch        # noqa
from simple_forums.backends.search.elastic_search import ElasticSearch  # noqa
from simple_forums.backends.search.simple_search import SimpleSearch    # noqa
