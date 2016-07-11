=======
History
=======

Pending Release
---------------

* New release notes here

1.2.0 (2016-07-11)
------------------

* Split all rule codes by type. This allows granular selection of the rules in
  flake8 configuration.

1.1.1 (2016-04-06)
------------------

* Fix crash on method calls

1.1.0 (2016-04-06)
------------------

* ``C401`` rule that complains about unnecessary list comprehensions inside
  calls to ``set()`` or ``dict()``.
* ``C402`` rule that complains about unnecessary list literals inside calls to
  ``set()`` or ``dict()``.

1.0.0 (2016-04-05)
------------------

* ``C400`` rule that complains about an unnecessary usage of a generator when a
  list/set/dict comprehension would do.
