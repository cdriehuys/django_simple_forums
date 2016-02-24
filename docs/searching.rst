=========
Searching
=========

Simple forums currently has a basic search engine that performs a keyword search over the titles of all the threads in the forum. In the future, there may be options to use a different search backend such as elasticsearch.

Simple Search
-------------
Class: ``simple_forums.backends.search.simple_search.SimpleSearch``

This backend performs searches by separating the search query into individual words, and then filtering the threads down to the ones that include all the keywords in their title. It does not rank results in any way. This can be useful if you don't need a complicated search engine.