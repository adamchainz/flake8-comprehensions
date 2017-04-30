=======
History
=======

Pending Release
---------------

* New release notes here
* Don't allow installation with Flake8 3.2.0 which doesn't enable the plugin.
  This bug was fixed in Flake8 3.2.1.
* Fix C402 false positive where a function call prevents using dict
  comprehension.

1.2.1 (2016-06-27)
------------------

* ``C407`` rule that complains about unnecessary list comprehensions inside
  builtins that can work on generators.

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
