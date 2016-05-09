from django.test import TestCase
from django.utils.safestring import SafeText

from simple_forums.backends import renderers


class TestBaseRenderer(TestCase):
    """ Test base rendering class """

    def setUp(self):
        """ Create renderer for each test """
        self.renderer = renderers.BaseRenderer()

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
        self.renderer = renderers.MarkdownRenderer()

    def test_basic_render(self):
        """ Test basic behavior.

        The 'render' method should convert markdown to html. For a
        basic string, this should wrap text in <p> tags.
        """
        text = "Some sample text"
        expected_html = "<p>Some sample text</p>"

        result = self.renderer.render(text)

        self.assertHTMLEqual(expected_html, result)

    def test_safe_string(self):
        """ Test that the output of the render method is marked safe.

        The output from MarkdownRenderer should be marked safe as it
        has been sanitized with the bleach library.
        """
        text = 'test'
        result = self.renderer.render(text)

        self.assertTrue(type(result) is SafeText)

    def test_script_tag(self):
        """ Test passing in text with a script tag.

        If a <script> tag is received in the input, it should be
        escaped.
        """
        text = "<script>alert('Hello, World!');</script>"

        expected_html = "&lt;script&gt;alert('Hello, World!');&lt;/script&gt;"

        self.assertHTMLEqual(expected_html, self.renderer.render(text))


class TestTextRenderer(TestCase):
    """ Test class for rendering plain text """

    def setUp(self):
        """ Create renderer for each test """
        self.renderer = renderers.TextRenderer()

    def test_basic_render(self):
        """ Test the basic behavior of the text renderer.

        Rendered text should be the same as the input text.
        """
        text = "Hello, World!"

        expected = "%s" % text

        self.assertEqual(expected, self.renderer.render(text))

    def test_rendered_not_safe(self):
        """ Test if the rendered string is marked as safe.

        The plain text renderer should have its contents autoescaped,
        so it should return a plain string instance, rather than an
        instance of SafeString.
        """
        text = 'test'
        rendered = self.renderer.render(text)

        self.assertTrue(type(rendered) is str)
