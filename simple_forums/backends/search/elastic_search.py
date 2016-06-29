from __future__ import absolute_import

from simple_forums import models
from simple_forums.backends.search import BaseSearch, SearchResultSet


class ElasticSearch(BaseSearch):
    """ Search backend using elasticsearch service """
    REQUIRED_SETTINGS = ['host', 'port']

    def __init__(self, *args, **kwargs):
        super(ElasticSearch, self).__init__(*args, **kwargs)

        host = self.connection_info['host']
        port = self.connection_info['port']

        from elasticsearch import Elasticsearch

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

        for message in thread.message_set.all():
            data = {
                'body': message.body,
            }

            self.es.index(
                index=self.index,
                doc_type='message',
                id=message.pk,
                body=data)

    def remove(self, thread):
        """ Remove the given object from the search index """
        assert isinstance(thread, models.Thread), \
            "'thread' is not a thread instance"

        self.es.delete(
            index=self.index,
            doc_type='thread',
            id=thread.pk)

        for message in thread.message_set.all():
            self.es.delete(
                index=self.index,
                doc_type='message',
                id=thread.pk)

    def search(self, query_string):
        """ Search for the given query string """
        body = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'match': {
                                'title': query_string,
                            },
                        },
                        {
                            'match': {
                                'body': query_string,
                            },
                        },
                    ]
                }
            }
        }

        search_results = self.es.search(
            index=self.index,
            doc_type='message,thread',
            body=body)

        hits = search_results.get('hits').get('hits')

        result_set = SearchResultSet()

        for hit in hits:
            id = hit.get('_id')
            doc_type = hit.get('_type')

            if doc_type == 'thread':
                obj = models.Thread.objects.get(id=id)
            elif doc_type == 'message':
                obj = models.Message.objects.get(id=id)

            score = hit.get('_score')
            result_set.add(obj, score)

        return result_set

    def wipe(self):
        """ Wipe the search index of all data """
        if self.es.indices.exists(self.index):
            self.es.indices.delete(self.index)
