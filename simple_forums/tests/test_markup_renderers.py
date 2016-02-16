from django.test import TestCase

from simple_forums import markup_renderers


class TestBaseRenderer(TestCase):
    """ Test base rendering class """

    def setUp(self):
        """ Create renderer for each test """
        self.renderer = markup_renderers.BaseRenderer()

    def test_render(self):
        """ Test the 'render' method.

        The 'render' method of the base class should raise a
        NotImplemented error.
        """
        text = "Some sample text"

        with self.assertRaises(NotImplementedError):
            self.renderer.render(text)


class TestMarkdownRenderer(TestCase):
    """ Test class for rendering markdown """

    def setUp(self):
        """ Create renderer for each test """
        self.renderer = markup_renderers.MarkdownRenderer()

    def test_basic_render(self):
        """ Test basic behavior.

        The 'render' method should convert markdown to html. For a
        basic string, this should wrap text in <p> tags.
        """
        text = "Some sample text"

        expected_html = "<p>Some sample text</p>"

        self.assertHTMLEqual(expected_html, self.renderer.render(text))

    def test_script_tag(self):
        """ Test passing in text with a script tag.

        If a <script> tag is received in the input, it should be
        escaped.
        """
        text = "<script>alert('Hello, World!');</script>"

        expected_html = "&lt;script&gt;alert('Hello, World!');&lt;/script&gt;"

        self.assertHTMLEqual(expected_html, self.renderer.render(text))
