Changelog
=========

v2.0
----
Backwards Incompatible Changes
  * Close `#47`_: Remove searching. Searching is best implemented by a
    third party app like `haystack` rather than trying to maintain
    additional features within this app.

v1.3.6
------
Bug Fixes
  * Fix `#51`_: Fixing issue where `<pre>` tags were escaped instead of rendered.

v1.3.5
------
Bug Fixes
  * Fix `#50`_: Adding `get_absolute_url` method to the `Topic` model.

v1.3.4
------
Bug Fixes
  * Fix issue where fix for `#41`_ didn't work in Django < 1.9

v1.3.3
------
Bug Fixes
  * Fix `#41`_: Using a namespace when including the app doesn't cause submitting forms to break

v1.3.1
------
Features
  * Close `#42`_: Allowing template tags to generate login/logout urls to take a view name as an optional parameter

v1.3.0
------
Features
  * Close `#12`_: Adding ids to comments so they can be linked to
  * Close `#28`_: Using django-admin-sortable to allow for re-ordering of topics in the admin interface
  * Close `#29`_: Adding the option to use elasticsearch for searching
  * Close `#32`_: Adding email notification system.

v1.2.0
------
Features
  * Close `#13`_: Adding ability to sort thread listing.

v1.1.1
------
Bug Fixes
  * Fix `#21`_: Specifying markdown output format as html5.
  * Fix `#24`_: Removing dependency on bleach-whitelist package.
General
  * Close `#25`_: Adding documentation for templates and searching.

v1.1.0
------
Features
  * Close `#18`_: Adding a basic search engine.

v1.0.9
------
Bug Fixes:
  * Fix `#23`_: Fixing issue where submitting a blank reply to a thread caused an error.

.. _#12: https://github.com/cdriehuys/django_simple_forums/issues/12
.. _#13: https://github.com/cdriehuys/django_simple_forums/issues/13
.. _#18: https://github.com/cdriehuys/django_simple_forums/issues/18
.. _#21: https://github.com/cdriehuys/django_simple_forums/issues/21
.. _#23: https://github.com/cdriehuys/django_simple_forums/issues/23
.. _#24: https://github.com/cdriehuys/django_simple_forums/issues/24
.. _#25: https://github.com/cdriehuys/django_simple_forums/issues/25
.. _#28: https://github.com/cdriehuys/django_simple_forums/issues/28
.. _#29: https://github.com/cdriehuys/django_simple_forums/issues/29
.. _#32: https://github.com/cdriehuys/django_simple_forums/issues/32
.. _#41: https://github.com/cdriehuys/django_simple_forums/issues/41
.. _#42: https://github.com/cdriehuys/django_simple_forums/issues/42
.. _#47: https://github.com/cdriehuys/django_simple_forums/issues/47
.. _#50: https://github.com/cdriehuys/django_simple_forums/issues/50
.. _#51: https://github.com/cdriehuys/django_simple_forums/issues/51
