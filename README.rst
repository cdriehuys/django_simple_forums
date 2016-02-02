=============
Simple Forums
=============

Installation
============

The easiest way to install simple forums is using pip::

	$ pip install django-simple-forums

Usage
=====

The following settings must be modified in ``settings.py``.

Add ``django.contrib.sites`` and ``simple_forums`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = [
		# default django apps
		'django.contrib.sites',
		...
		'simple_forums',
		...
	]

Add the sites middleware to ``MIDDLEWARE_CLASSES``::

	MIDDLEWARE_CLASSES = [
		# default django middleware classes
		'django.contrib.sites.middleware.CurrentSiteMiddlware',
	]

After migrating your database (``./manage.py migrate``), go to the admin, and create a new site model (or modify the existing one). Once you've done that, you need to find the id of your site. This can be done through the shell::

	$ ./manage.py shell

	>>> from django.contrib.sites.models import Site
	>>> s = Site.objects.get()
	>>> s.id
	1

Then, back in ``settings.py``, set ``SITE_ID`` to the id of your site.::
	
	# example
	SITE_ID = 1

In order to use the views in the package, you must include the url patterns for the forums in ``urls.py``::

	url_patterns = [
		...
		url(r'^forums/', include('simple_forums.urls')),
		...
	]