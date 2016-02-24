from django.test import TestCase

from simple_forums import models
from simple_forums.backends.search import simple_search
from simple_forums.tests.testing_utils import create_thread


class TestSimpleSearch(TestCase):
    """ Test simple ORM based search """

    def setUp(self):
        """ Initialize a backend for each test """
        self.backend = simple_search.SimpleSearch()

    def test_blank_search(self):
        """ Test result of searching for a blank string.

        Searching for a blank string should return all threads.
        """
        create_thread(title='thread 1')
        create_thread(title='thread 2')

        expected = list()
        for thread in models.Thread.objects.all():
            expected.append('<Thread: %s>' % thread)

        self.assertQuerysetEqual(
            self.backend.search(''),
            expected,
            ordered=False)

    def test_full_title_search(self):
        """ Test searching for the title of a thread.

        Searching for the title of a thread should return only that
        thread.
        """
        create_thread(title='cat')
        create_thread(title='dog')

        self.assertQuerysetEqual(
            self.backend.search('cat'),
            ['<Thread: cat>'])

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

        expected = ['<Thread: %s>' % thread for thread in (t1, t2, t3)]

        self.assertQuerysetEqual(
            self.backend.search('funny cat'),
            expected,
            ordered=False)

    def test_partial_title_match(self):
        """ Test search that matches multiple threads.

        If a search matches multiple threads, all matching threads
        should be returned.
        """
        t1 = create_thread(title='cat escapes prison')
        t2 = create_thread(title='woman finds cat playing with yarn')
        create_thread(title='stray dog wins lottery')

        self.assertQuerysetEqual(
            self.backend.search('cat'),
            ['<Thread: %s>' % t1, '<Thread: %s>' % t2],
            ordered=False)
