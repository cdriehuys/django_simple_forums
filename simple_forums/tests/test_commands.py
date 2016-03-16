import json

from django.core.management import call_command
from django.test import override_settings, TestCase
from django.utils.six import StringIO

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from simple_forums.backends.search import ElasticSearch
from simple_forums.tests.testing_utils import create_thread


es_settings = {
    'search_class': 'simple_forums.backends.search.ElasticSearch',
    'host': 'localhost',
    'port': 9200,
    'index': 'test',
}


class TestUpdateIndex(TestCase):

    def setUp(self):
        """ Create StringIO for command output """
        self.out = StringIO()

    @override_settings(SIMPLE_FORUMS={'search_backend': es_settings})
    def test_update(self):
        """ Test updating search index with threads.

        Updating the index should add all existing threads to the index.
        """
        thread = create_thread()

        call_command('updateindex', stdout=self.out)

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        source = es.get_source(
            index='test',
            doc_type='thread',
            id=thread.pk)
        source_json = json.dumps(source)

        expected = {
            'title': thread.title,
        }
        expected_json = json.dumps(expected)

        self.assertJSONEqual(expected_json, source_json)
        self.assertIn("Updated 1 thread(s)", self.out.getvalue())

    def test_update_no_threads(self):
        """ Test updating the index with no thread instances.

        If there are no threads, the command should display a warning
        that there are no threads to index.
        """
        call_command('updateindex', stdout=self.out)

        self.assertIn('There are no threads to index', self.out.getvalue())

    @override_settings(SIMPLE_FORUMS={'search_backend': es_settings})
    def test_update_old_threads(self):
        """ Test updating the index with old threads.

        If there was a thread that was previously in the index and has
        since been deleted, then it should be removed from the index.
        """
        thread = create_thread()
        thread_pk = thread.pk

        backend = ElasticSearch()
        backend.add(thread)

        thread.delete()

        call_command('updateindex', stdout=self.out)

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        with self.assertRaises(NotFoundError):
            es.get_source(
                index='test',
                doc_type='thread',
                id=thread_pk)
