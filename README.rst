=============
Simple Forums
=============

Installation
============

The easiest way to install simple forums is using pip::

	$ pip install git+https://github.com/smalls12/django_simple_forums#egg=simple_forums

Usage
=====

First, add ``simple_forums`` to your ``INSTALLED_APPS``::

	INSTALLED_APPS = [
		...
		'simple_forums',
		...
	]

Then, include the url patterns for the forum in your ``urls.py``::

	url_patterns = [
		...
		url(r'^forums', include('simple_forums.urls')),
		...
	]