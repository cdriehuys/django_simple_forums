=============
Configuration
=============

All configuration options for simple forums should be placed in a dictionary called ``SIMPLE_FORUMS`` in ``settings.py``. Example::

    SIMPLE_FORUMS = {
        'markup_renderer': 'simple_forums.markup_renderers.MarkdownRenderer',
    }

Available Settings
------------------

markdown_extensions (=['pymdownx.github'])
  A list of extensions to process markdown with. Only has an effect if ``MarkdownRenderer`` is used. The default list of extensions is defined in ``simple_forums.markup_renderers.MarkdownRenderer.DEFAULT_EXTENSIONS``.

markup_renderer (='simple_forums.markup_renderers.TextRenderer')
  This class specifies which form of markup should be used to render posts. Currently there is a choice between plain text and Markdown.

  Choices:
    * ``'simple_forums.markup_renderers.MarkdownRenderer'``
    * ``'simple_forums.markup_renderers.TextRenderer'``