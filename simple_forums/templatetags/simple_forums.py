from django import template
from django.core.urlresolvers import reverse
from django.template.defaultfilters import urlencode
from django.utils.safestring import mark_safe

from simple_forums.markup_renderers import markdown


register = template.Library()


@register.simple_tag(takes_context=True)
def login_url(context):
    """ Construct a login url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse('login'),
        urlencode(request.path))


@register.simple_tag(takes_context=True)
def logout_url(context):
    """ Construct a logout url that redirects to the current page. """
    request = context.get('request')
    return '%s?next=%s' % (
        reverse('logout'),
        urlencode(request.path))


@register.simple_tag
def render_markup(text):
    """ Render text using the renderer specified in settings.py """
    renderer = markdown.MarkdownRenderer()

    return mark_safe(renderer.render(text))
