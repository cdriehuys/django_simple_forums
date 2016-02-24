import bleach

from django.utils.safestring import mark_safe

from markdown import markdown

from simple_forums.utils import get_setting


class BaseRenderer:
    """ Base class that all renderers are based on """

    def render(self, text):
        """ Render marked up text as html """
        raise NotImplementedError


class MarkdownRenderer(BaseRenderer):
    """ Handles rendering markdown into html """

    DEFAULT_EXTENSIONS = [
        'pymdownx.github',
    ]

    # Attributes and tags used for rendering markdown taken from:
    # https://github.com/yourcelf/bleach-whitelist
    #
    # Slightly modified

    MARKDOWN_ATTRS = {
        'a': ['alt', 'href', 'title'],
        'img': ['alt', 'src', 'title'],
    }

    MARKDOWN_TAGS = {
        'a',
        'b', 'blockquote', 'br',
        'code',
        'dd', 'div', 'dt',
        'em',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
        'i', 'img',
        'li',
        'ol',
        'p',
        'span', 'strong',
        'tt',
        'ul',
    }

    @staticmethod
    def get_extensions():
        """ Get a list of extensions to use """
        return get_setting(
            'markdown_extensions',
            MarkdownRenderer.DEFAULT_EXTENSIONS)

    def render(self, text):
        """ Convert the given text into html """
        converted = markdown(
            text,
            extensions=MarkdownRenderer.get_extensions())

        cleaned = bleach.clean(
            converted,
            attributes=self.MARKDOWN_ATTRS,
            tags=self.MARKDOWN_TAGS)

        return mark_safe(cleaned)


class TextRenderer(BaseRenderer):
    """ Renders text as itself """

    def render(self, text):
        """ Return the text """
        return text
