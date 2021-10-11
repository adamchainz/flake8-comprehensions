=======
History
=======

3.7.0 (2021-10-11)
------------------

* Support Flake8 4.

3.6.1 (2021-08-16)
------------------

* Fix type hint for ``tree`` argument.

  Thanks to kasium for the report in `Issue #352
  <https://github.com/adamchainz/flake8-comprehensions/issues/352>`__.

3.6.0 (2021-08-13)
------------------

* Add type hints.

3.5.0 (2021-05-10)
------------------

* Support Python 3.10.

* Stop distributing tests to reduce package size. Tests are not intended to be
  run outside of the tox setup in the repository. Repackagers can use GitHub's
  tarballs per tag.

3.4.0 (2021-03-18)
------------------

* Remove rules C407 (Unnecessary ``<dict/list>`` comprehension - ``<builtin>``
  can take a generator) and C412 (Unnecessary ``<dict/list/set>`` comprehension
  - 'in' can take a generator). Both rules recommended increasing laziness,
  which is not always desirable and can lead to subtle bugs. Also, a fully
  exhausted generator is slower than an equivalent comprehension, so the advice
  did not always improve performance.

  Thanks to David Smith, Dylan Young, and Leonidas Loucas for the report in
  `Issue #247
  <https://github.com/adamchainz/flake8-comprehensions/issues/247>`__.

3.3.1 (2020-12-19)
------------------

* Drop Python 3.5 support.
* Improved installation instructions in README.

3.3.0 (2020-10-23)
------------------

* Support Python 3.9.
* Move license from ISC to MIT License.
* Partially reverted the change to ``C408`` to make it apply again to when
  ``dict`` is called with keyword arguments, e.g. ``dict(a=1, b=2)`` will be
  flagged to be rewritten in the literal form ``{"a": 1, "b": 2}``

3.2.3 (2020-06-06)
------------------

* Made ``C408`` only apply when no arguments are passed to
  ``dict``/``list``/``tuple``.

3.2.2 (2020-01-20)
------------------

* Remove check for dict comprehensions in rule C407 as it would also change the
  results for certain builtins such as ``sum()``.

3.2.1 (2020-01-20)
------------------

* Remove check for set comprehensions in rule C407 as it would change the
  results for certain builtins such as ``sum()``.

3.2.0 (2020-01-20)
------------------

* Add ``filter`` and ``map`` to rule C407.
* Check for dict and set comprehensions in rules C407 and C412.

3.1.4 (2019-11-20)
------------------

* Remove the tuple/unpacking check from C416 to prevent false positives where
  the type of the iterable is changed from some iterable to a tuple.

3.1.3 (2019-11-19)
------------------

* Ensure the fix for false positives in ``C416`` rule for asynchronous
  comprehensions runs on Python 3.6 too.

3.1.2 (2019-11-18)
------------------

* Fix false positives in ``C416`` rule for list comprehensions returning
  tuples.

3.1.1 (2019-11-16)
------------------

* Fix false positives in ``C416`` rule for asynchronous comprehensions.

3.1.0 (2019-11-15)
------------------

* Update Python support to 3.5-3.8.
* Fix false positives for C404 for list comprehensions not directly creating
  tuples.
* Add ``C413`` rule that checks for unnecessary use of ``list()`` or
  ``reversed()`` around ``sorted()``.
* Add ``C414`` rule that checks for unnecessary use of the following:
    * ``list()``, ``reversed()``, ``sorted()``, or ``tuple()``  within ``set``
      or ``sorted()``
    * ``list()`` or ``tuple()``  within ``list()`` or ``tuple()``
    * ``set()``  within ``set``
* Add ``C415`` rule that checks for unnecessary reversal of an iterable via
  subscript within ``reversed()``, ``set()``, or ``sorted()``.
* Add ``C416`` rule that checks for unnecessary list or set comprehensions that
  can be rewritten using ``list()`` or ``set()``.

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
