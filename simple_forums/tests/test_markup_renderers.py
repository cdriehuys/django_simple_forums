from django.test import TestCase

from simple_forums.markup_renderers import base


class TestBaseRenderer(TestCase):
    """ Test base rendering class """

    def test_render(self):
        """ Test the 'render' method.

        The 'render' method of the base class should raise a
        NotImplemented error.
        """
        renderer = base.BaseRenderer()
        text = "Some sample text"

        with self.assertRaises(NotImplementedError):
            renderer.render(text)
