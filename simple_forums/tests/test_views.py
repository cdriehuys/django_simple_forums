from django.core.urlresolvers import reverse
from django.test import TestCase

from simple_forums import models
from simple_forums.tests.testing_utils import create_message, create_thread


class TestThreadDetailView(TestCase):
    """ Tests for ThreadDetailView """

    @staticmethod
    def get_detail_url(pk):
        """ Get the url of the thread detail view for the given thread.

        Determines the url of the thread detail view using the thread's
        pk and slug.
        """
        thread = models.Thread.objects.get(pk=pk)

        kwargs = {
            'pk': thread.pk,
            'thread_slug': thread.slug,
        }

        return reverse('thread-detail', kwargs=kwargs)

    def test_no_messages(self):
        """ Test the view when the given thread has no messages.

        If the thread has no messages, the response should contain a
        note to the user that there are no messages for the current
        thread.

        In practice, this should never occur because when threads are
        created, there should always be an initial message.
        """
        thread = create_thread()

        url = self.get_detail_url(thread.pk)
        response = self.client.get(url)

        no_replies_message = "There are no replies to this thread"

        self.assertEqual(200, response.status_code)
        self.assertEqual(thread, response.context['thread'])
        self.assertContains(response, no_replies_message)

    def test_with_message(self):
        """ Test the view when the given thread has a message.

        If the thread has a message, it should be displayed following
        the thread's title.
        """
        thread = create_thread()
        message = create_message(thread=thread)

        url = self.get_detail_url(thread.pk)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertContains(response, message.body)


class TestThreadListView(TestCase):
    """ Tests for ThreadListView """

    URL = reverse('thread-list')

    def test_no_threads(self):
        """ Test the view when there are no threads.

        If there are no threads, then the view should display a message
        that there are no threads.
        """
        response = self.client.get(self.URL)

        empty_message = "No threads found"

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            [])
        self.assertContains(response, empty_message)

    def test_thread(self):
        """ Test view when there is a thread.

        If there is a thread, then the view should show the thread's
        name.
        """
        thread = create_thread()

        response = self.client.get(self.URL)

        thread_detail_url = reverse('thread-detail', kwargs={
            'pk': thread.pk,
            'thread_slug': thread.slug
            })
        href_text = 'href="%s"' % thread_detail_url

        self.assertEqual(200, response.status_code)
        self.assertQuerysetEqual(
            response.context['thread_list'],
            ['<Thread: %s>' % thread.title])
        self.assertContains(response, thread.title)
        self.assertContains(response, href_text)
