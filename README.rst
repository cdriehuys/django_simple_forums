=============
Simple Forums
=============

Important Note
==============

This package is currently in early alpha. This means that backwards incompatible changes can be introduced at any time as described `here <http://semver.org/#spec-item-4>`_.

Installation
============

The easiest way to install simple forums is using pip::

	$ pip install django-simple-forums

Usage
=====

The following settings must be modified in ``settings.py``.

Add ``simple_forums`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = [
		# default django apps
		...
		'simple_forums',
		...
		# your custom apps
	]

In order to use the views included in simple forums, you must include the url patterns for the forums in your ``urls.py``::

	url_patterns = [
		...
		url(r'^forums/', include('simple_forums.urls')),
		...
	]