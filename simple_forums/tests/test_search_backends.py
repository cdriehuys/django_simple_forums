import json

from django.test import override_settings, TestCase

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError

from simple_forums import models
from simple_forums.backends import search
from simple_forums.tests.testing_utils import create_thread


elasticsearch_settings = {
    'search_class': 'simple_forums.backends.search.ElasticSearch',
    'host': 'localhost',
    'port': 9200,
    'index': 'test',
}


class TestBaseSearch(TestCase):
    """ Test base search class """

    def setUp(self):
        self.backend = search.BaseSearch()

    def test_add(self):
        """ Test adding an object to the index.

        The base search backend should raise a NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            self.backend.add(None)

    def test_remove(self):
        """ Test removing an object from the index.

        The base search backend should raise a NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            self.backend.remove(None)

    def test_search(self):
        """ Test behavior when searching.

        The base search engine should raise a NotImplementedError.
        """
        with self.assertRaises(NotImplementedError):
            self.backend.search('test')


@override_settings(SIMPLE_FORUMS={'search_backend': elasticsearch_settings})
class TestElasticSearch(TestCase):
    """ Test elasticsearch based search """

    def setUp(self):
        self.backend = search.ElasticSearch()

    def tearDown(self):
        """ Clean up elasticsearch test index """
        if self.backend.es.indices.exists('test'):
            self.backend.es.indices.delete('test')

    def test_add(self):
        """ Test adding an object to the search index.

        Adding an object to the search index should make it searchable
        by elasticsearch.
        """
        thread = create_thread()
        self.backend.add(thread)

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        source = es.get_source(
            index=self.backend.index,
            doc_type='thread',
            id=thread.pk)
        source_json = json.dumps(source)

        expected = {
            'title': thread.title,
        }
        expected_json = json.dumps(expected)

        self.assertJSONEqual(expected_json, source_json)

    def test_add_non_thread(self):
        """ Test adding a non-thread object.

        Adding a non-thread object to the search index should result in
        an assertion error.
        """
        with self.assertRaises(AssertionError):
            self.backend.add(3)

    def test_remove(self):
        """ Test removing an object from the search index.

        Removing an object from the search index should make it
        inaccessible to elasticsearch.
        """
        thread = create_thread()
        self.backend.add(thread)
        self.backend.remove(thread)

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        with self.assertRaises(NotFoundError):
            es.get_source(
                index=self.backend.index,
                doc_type='thread',
                id=thread.pk)

    def test_remove_invalid_pk(self):
        """ Test removing an object that is not in the index.

        Removing an object that is not in the index should raise a
        NotFoundError
        """
        thread = create_thread()
        self.backend.add(thread)
        self.backend.remove(thread)
        # try removing it after it's been removed
        with self.assertRaises(NotFoundError):
            self.backend.remove(thread)

    def test_search(self):
        """ Test searching for a term.

        Searching for a term should bring up threads with titles
        similar to the search query.
        """
        thread1 = create_thread(title='Darth Vader')
        thread2 = create_thread(title='dartheaven.com')
        thread3 = create_thread(title='Darth Maul')

        self.backend.add(thread1)
        self.backend.add(thread2)
        self.backend.add(thread3)

        raw_results = self.backend.search('darth vader')
        results = [thread for thread, _ in raw_results]

        expected = [
            '<Thread: %s>' % thread1,
            '<Thread: %s>' % thread3,
        ]

        self.assertQuerysetEqual(results, expected)


class TestSimpleSearch(TestCase):
    """ Test simple ORM based search """

    def setUp(self):
        """ Initialize a backend for each test """
        self.backend = search.SimpleSearch()

    def test_add(self):
        """ Test adding an object to the search index.

        This method should raise a warning that the behavior is not
        implemented.
        """
        with self.assertWarns(Warning) as context:
            self.backend.add(None)

        self.assertEqual(
            'add is not implemented in this backend',
            context.warning.args[-1])

    def test_blank_search(self):
        """ Test result of searching for a blank string.

        Searching for a blank string should return all threads.
        """
        create_thread(title='thread 1')
        create_thread(title='thread 2')

        results = [t for t, _ in self.backend.search('')]

        expected = list()
        for thread in models.Thread.objects.all():
            expected.append(thread)

        self.assertEqual(expected, results)

    def test_full_title_search(self):
        """ Test searching for the title of a thread.

        Searching for the title of a thread should return only that
        thread.
        """
        thread = create_thread(title='cat')
        create_thread(title='dog')

        results = [thread for thread, _ in self.backend.search('cat')]

        self.assertEqual([thread], results)

    def test_multiple_keywords(self):
        """ Test searching for multiple words.

        If the query string contains multiple words, all threads whose
        title contains those words should be returned.
        """
        t1 = create_thread(title='funny cat')
        t2 = create_thread(title='cat funny')
        t3 = create_thread(title='funny video of a cat')
        create_thread(title='cat')
        create_thread(title='funny')

        results = [thread for thread, _ in self.backend.search('funny cat')]
        expected = [t1, t2, t3]

        self.assertEqual(expected, results)

    def test_partial_title_match(self):
        """ Test search that matches multiple threads.

        If a search matches multiple threads, all matching threads
        should be returned.
        """
        t1 = create_thread(title='cat escapes prison')
        t2 = create_thread(title='woman finds cat playing with yarn')
        create_thread(title='stray dog wins lottery')

        results = [t for t, _ in self.backend.search('cat')]
        expected = [t1, t2]

        self.assertEqual(expected, results)

    def test_remove(self):
        """ Test removing an object from the search index.

        This method should raise a warning that the behavior is not
        implemented.
        """
        with self.assertWarns(Warning) as context:
            self.backend.remove(None)

        self.assertEqual(
            'remove is not implemented in this backend',
            context.warning.args[-1])
