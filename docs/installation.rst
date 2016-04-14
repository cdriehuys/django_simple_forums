============
Installation
============

Django
======

Download
--------

The easiest way to install simple forums is as a python package through pip::
    
    $ pip install django-simple-forums

Installing
----------

In ``settings.py``::

    INSTALLED_APPS = [
        ...
        # default django apps
        'adminsortable',
        'simple_forums',

        # If you want email notification functionality, add the following:
        'simple_forums.notifications',
        ...
    ]

If you would like an easy way to keep track of installed apps within your templates, add the following context processor (in ``settings.py``)::

    TEMPLATES = [
        {
            'OPTIONS': {
                'context_processors': [
                    # other context processors
                    'simple_forums.context_processors.installed_apps',
                ],
            },
        },
    ]

In ``urls.py``::

    urlpatterns = [
        ...
        url(r'^forums/', include('simple_forums.urls')),
        ...
    ]

Post-Installation
=================

Apply the migrations for simple forums::

    $ ./manage.py migrate

On your server, visit the admin page and start creating topics for users to post under.