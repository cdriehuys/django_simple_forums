import bleach

from bleach_whitelist.bleach_whitelist import markdown_attrs, markdown_tags

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
            tags=markdown_tags + ['pre'],
            attributes=markdown_attrs)

        return mark_safe(cleaned)


class TextRenderer(BaseRenderer):
    """ Renders text as itself """

    def render(self, text):
        """ Return the text """
        return text
