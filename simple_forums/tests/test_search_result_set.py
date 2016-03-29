from django.test import TestCase

from simple_forums.backends.search import SearchResultSet
from simple_forums.tests.testing_utils import create_thread


class TestSearchResultSet(TestCase):
    """ Test class used to return search results """

    def test_add(self):
        """ Test adding a result to the result set.

        Adding a thread to the result set with it's score should save
        the thread in the result set.
        """
        thread = create_thread()
        result_set = SearchResultSet()
        result_set.add(thread, 0)

        self.assertEqual((thread, 0), result_set[0])

    def test_add_default_score(self):
        """ Test adding a result to the result set with no score.

        Adding a thread to the result set and not specifying a score
        should set the result's score to 0.
        """
        thread = create_thread()
        result_set = SearchResultSet()
        result_set.add(thread)

        self.assertEqual((thread, 0), result_set[0])

    def test_get_sorted(self):
        """ Test getting the sorted results.

        The results should be ordered by score, descending.
        """
        result_set = SearchResultSet()
        result_set.results = [
            (None, 1),
            (None, 0),
            (None, 3),
        ]

        expected = [
            (None, 3),
            (None, 1),
            (None, 0),
        ]

        self.assertEqual(expected, result_set.get_sorted())
