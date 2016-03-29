=========
Searching
=========

Simple forums currently has a basic search engine that performs a keyword search over the titles of all the threads in the forum as well as the option to use the third party search engine `elasticsearch`_.

Simple Search
-------------
Class: ``simple_forums.backends.search.SimpleSearch``

This backend performs searches by separating the search query into individual words, and then filtering the threads down to the ones that include all the keywords in their title. It does not rank results in any way. This can be useful if you don't need a complicated search engine.

Configuration Options:
  None

Elasticsearch
-------------
Class: ``simple_forums.backends.search.ElasticSearch``

**Requires Installation of the** `elasticsearch-py`_ **package.**

This backend connects to an elasticsearch server using the given credentials and uses it to perform searches. It is much more powerful than the Simple Search backend because it has the ability to search through replies to threads rather than just the thread titles.

Configuration Options:
  **host** (Required): The hostname of the elasticsearch server
  
  **port** (Required): The port to connect to the elasticsearch server on
  
  **index**: The name of the elasticsearch index to use


.. _elasticsearch: https://www.elastic.co/
.. _elasticsearch-py: https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html