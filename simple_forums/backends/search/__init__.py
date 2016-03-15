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
from simple_forums.backends.search.elasticsearch import ElasticSearch   # noqa
from simple_forums.backends.search.simple_search import SimpleSearch    # noqa
