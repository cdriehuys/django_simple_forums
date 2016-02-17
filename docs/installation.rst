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

        'simple_forums',
        ...
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