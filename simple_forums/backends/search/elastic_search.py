from elasticsearch import Elasticsearch

from simple_forums import models
from simple_forums.backends.search import BaseSearch, SearchResultSet


class ElasticSearch(BaseSearch):
    """ Search backend using elasticsearch service """
    REQUIRED_SETTINGS = ['host', 'port']

    def __init__(self, *args, **kwargs):
        super(ElasticSearch, self).__init__(*args, **kwargs)

        host = self.connection_info['host']
        port = self.connection_info['port']

        self.es = Elasticsearch([{'host': host, 'port': port}])

        # get index name or use default of 'forums'
        self.index = self.connection_settings.get('index', 'forums')

    def add(self, thread):
        """ Add the given object to the search index """
        assert isinstance(thread, models.Thread), "Can only index threads"

        data = {
            'title': thread.title,
        }

        self.es.index(
            index=self.index,
            doc_type='thread',
            id=thread.pk,
            body=data)

    def remove(self, thread):
        """ Remove the given object from the search index """
        assert isinstance(thread, models.Thread), \
            "'thread' is not a thread instance"

        self.es.delete(
            index=self.index,
            doc_type='thread',
            id=thread.pk)

    def search(self, query_string):
        """ Search for the given query string """
        body = {
            'query': {
                'match': {
                    'title': query_string,
                }
            }
        }

        search_results = self.es.search(
            index=self.index,
            doc_type='thread',
            body=body)
        hits = search_results.get('hits').get('hits')

        result_set = SearchResultSet()

        for hit in hits:
            id = hit.get('_id')
            thread = models.Thread.objects.get(id=id)
            score = hit.get('_score')
            result_set.add(thread, score)

        return result_set

    def wipe(self):
        """ Wipe the search index of all data """
        if self.es.indices.exists(self.index):
            self.es.indices.delete(self.index)
