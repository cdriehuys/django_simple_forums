Changelog
=========

v2.0
----
Backwards Incompatible Changes
  * Close #47: Remove searching. Searching is best implemented by a
    third party app like ``haystack`` rather than trying to maintain
    additional features within this app.

v1.3.6
------
Bug Fixes
  * Fix #51: Fixing issue where ``<pre>`` tags were escaped instead of rendered.

v1.3.5
------
Bug Fixes
  * Fix #50: Adding ``get_absolute_url`` method to the ``Topic`` model.

v1.3.4
------
Bug Fixes
  * Fix issue where fix for #41 didn't work in Django < 1.9

v1.3.3
------
Bug Fixes
  * Fix #41: Using a namespace when including the app doesn't cause submitting forms to break

v1.3.1
------
Features
  * Close #42: Allowing template tags to generate login/logout urls to take a view name as an optional parameter

v1.3.0
------
Features
  * Close #12: Adding ids to comments so they can be linked to
  * Close #28: Using django-admin-sortable to allow for re-ordering of topics in the admin interface
  * Close #29: Adding the option to use elasticsearch for searching
  * Close #32: Adding email notification system.

v1.2.0
------
Features
  * Close #13: Adding ability to sort thread listing.

v1.1.1
------
Bug Fixes
  * Fix #21: Specifying markdown output format as html5.
  * Fix #24: Removing dependency on ``bleach-whitelist`` package.
General
  * Close #25: Adding documentation for templates and searching.

v1.1.0
------
Features
  * Close #18: Adding a basic search engine.

v1.0.9
------
Bug Fixes:
  * Fix #23: Fixing issue where submitting a blank reply to a thread caused an error.
