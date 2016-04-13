from django.conf import settings


def installed_apps(request):
    check_installed = {
        # short name: full app name
        'notifications': 'simple_forums.notifications',
    }

    context = {
        'installed_apps': settings.INSTALLED_APPS,
    }

    for app, full_name in check_installed.items():
        context['%s_installed' % app] = full_name in settings.INSTALLED_APPS

    return context
