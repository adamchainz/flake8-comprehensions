=======
History
=======

3.0.1 (2019-10-28)
------------------

* Fix version display on ``flake8 --version`` (removing dependency on
  ``cached-property``). Thanks to Jon Dufresne.

3.0.0 (2019-10-25)
------------------

* Update Flake8 support to 3.0+ only. 3.0.0 was released in 2016 and the plugin
  hasn't been tested with it since.

2.3.0 (2019-10-25)
------------------

* Converted setuptools metadata to configuration file. This meant removing the
  ``__version__`` attribute from the package. If you want to inspect the
  installed version, use
  ``importlib.metadata.version("flake8-comprehensions")``
  (`docs <https://docs.python.org/3.8/library/importlib.metadata.html#distribution-versions>`__ /
  `backport <https://pypi.org/project/importlib-metadata/>`__).
* Add dependencies on ``cached-property`` and ``importlib-metadata``.
* Fix false negatives in ``C407`` for cases when ``enumerate`` and ``sum()``
  are passed more than one argument.

2.2.0 (2019-08-12)
------------------

* Update Python support to 3.5-3.7, as 3.4 has reached its end of life.
* ``C412`` rule that complains about using list comprehension with ``in``.

2.1.0 (2019-03-01)
------------------

* Add missing builtin ``enumerate`` to ``C407``.

2.0.0 (2019-02-02)
------------------

* Drop Python 2 support, only Python 3.4+ is supported now.

1.4.1 (2017-05-17)
------------------

* Fix false positives in ``C408`` for calls using ``*args`` or ``**kwargs``.

1.4.0 (2017-05-14)
------------------

* Plugin now reserves the full ``C4XX`` code space rather than just ``C40X``
* ``C408`` rule that complains about using ``tuple()``, ``list()``, or
  ``dict()`` instead of a literal.
* ``C409`` and ``C410`` rules that complain about an unnecessary list or tuple
  that could be rewritten as a literal.
* ``C411`` rule that complains about using list comprehension inside a
  ``list()`` call.

1.3.0 (2017-05-01)
------------------

* Don't allow installation with Flake8 3.2.0 which doesn't enable the plugin.
  This bug was fixed in Flake8 3.2.1.
* Prevent false positives of ``C402`` from generators of expressions that
  aren't two-tuples.
* ``C405`` and ``C406`` now also complain about unnecessary tuple literals.

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
