=====================
flake8-comprehensions
=====================

.. image:: https://img.shields.io/github/workflow/status/adamchainz/flake8-comprehensions/CI/main?style=for-the-badge
   :target: https://github.com/adamchainz/flake8-comprehensions/actions?workflow=CI

.. image:: https://img.shields.io/pypi/v/flake8-comprehensions.svg?style=for-the-badge
   :target: https://pypi.org/project/flake8-comprehensions/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge
   :target: https://github.com/psf/black

.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit

A `flake8 <https://flake8.readthedocs.io/en/latest/index.html>`_ plugin that helps you write better list/set/dict comprehensions.

Requirements
============

Python 3.6 to 3.10 supported.

Installation
============

First, install with ``pip``:

.. code-block:: sh

     python -m pip install flake8-comprehensions

Second, check that ``flake8`` lists the plugin in its version line:

.. code-block:: sh

    $ flake8 --version
    3.7.8 (flake8-comprehensions: 3.0.0, mccabe: 0.6.1, pycodestyle: 2.5.0, pyflakes: 2.1.1) CPython 3.8.0 on Linux

Third, add the ``C4`` prefix to your `select list <https://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-select>`__.
For example, if you have your configuration in ``setup.cfg``:

.. code-block:: ini

    [flake8]
    select = E,F,W,C4

----

**Linting a Django project?**
Check out my book `Speed Up Your Django Tests <https://gumroad.com/l/suydt>`__ which covers loads of best practices so you can write faster, more accurate tests.

----

Rules
=====

C400-402: Unnecessary generator - rewrite as a ``<list/set/dict>`` comprehension.
---------------------------------------------------------------------------------

It's unnecessary to use ``list``, ``set``, or ``dict`` around a generator expression, since there are equivalent comprehensions for these types.
For example:

* Rewrite ``list(f(x) for x in foo)`` as ``[f(x) for x in foo]``
* Rewrite ``set(f(x) for x in foo)`` as ``{f(x) for x in foo}``
* Rewrite ``dict((x, f(x)) for x in foo)`` as ``{x: f(x) for x in foo}``

C403-404: Unnecessary list comprehension - rewrite as a ``<set/dict>`` comprehension.
-------------------------------------------------------------------------------------

It's unnecessary to use a list comprehension inside a call to ``set`` or ``dict``, since there are equivalent comprehensions for these types.
For example:

* Rewrite ``set([f(x) for x in foo])`` as ``{f(x) for x in foo}``
* Rewrite ``dict([(x, f(x)) for x in foo])`` as ``{x: f(x) for x in foo}``

C405-406: Unnecessary ``<list/tuple>`` literal - rewrite as a ``<set/dict>`` literal.
-------------------------------------------------------------------------------------

It's unnecessary to use a list or tuple literal within a call to ``set`` or ``dict``.
For example:

* Rewrite ``set([1, 2])`` as ``{1, 2}``
* Rewrite  ``set((1, 2))`` as ``{1, 2}``
* Rewrite ``set([])`` as ``set()``
* Rewrite ``dict([(1, 2)])`` as ``{1: 2}``
* Rewrite ``dict(((1, 2),))`` as ``{1: 2}``
* Rewrite ``dict([])`` as ``{}``

C408: Unnecessary ``<dict/list/tuple>`` call - rewrite as a literal.
--------------------------------------------------------------------

It's slower to call e.g. ``dict()`` than using the empty literal, because the name ``dict`` must be looked up in the global scope in case it has been rebound.
Same for the other two basic types here.
For example:

* Rewrite ``dict()`` as ``{}``
* Rewrite ``dict(a=1, b=2)`` as ``{"a": 1, "b": 2}``
* Rewrite ``list()`` as ``[]``
* Rewrite ``tuple()`` as ``()``

C409-410: Unnecessary ``<list/tuple>`` passed to ``<list/tuple>``\() - (remove the outer call to ``<list/tuple>``()/rewrite as a ``<list/tuple>`` literal).
-----------------------------------------------------------------------------------------------------------------------------------------------------------

It's unnecessary to use a list or tuple literal within a call to ``list`` or ``tuple``, since there is literal syntax for these types.
For example:

* Rewrite ``tuple([1, 2])`` as ``(1, 2)``
* Rewrite ``tuple((1, 2))`` as ``(1, 2)``
* Rewrite ``tuple([])`` as ``()``
* Rewrite ``list([1, 2])`` as ``[1, 2]``
* Rewrite ``list((1, 2))`` as ``[1, 2]``
* Rewrite ``list([])`` as ``[]``

C411: Unnecessary list call - remove the outer call to list().
--------------------------------------------------------------

It's unnecessary to use a ``list`` around a list comprehension, since it is equivalent without it.
For example:

* Rewrite ``list([f(x) for x in foo])`` as ``[f(x) for x in foo]``

C413: Unnecessary ``<list/reversed>`` call around sorted().
-----------------------------------------------------------

It's unnecessary to use ``list()`` around ``sorted()`` as it already returns a list.
It is also unnecessary to use ``reversed()`` around ``sorted()`` as the latter has a ``reverse`` argument.
For example:

* Rewrite ``list(sorted([2, 3, 1]))`` as ``sorted([2, 3, 1])``
* Rewrite ``reversed(sorted([2, 3, 1]))`` as ``sorted([2, 3, 1], reverse=True)``
* Rewrite ``reversed(sorted([2, 3, 1], reverse=True))`` as ``sorted([2, 3, 1])``

C414: Unnecessary ``<list/reversed/set/sorted/tuple>`` call within ``<list/set/sorted/tuple>``\().
--------------------------------------------------------------------------------------------------

It's unnecessary to double-cast or double-process iterables by wrapping the listed functions within ``list``/``set``/``sorted``/``tuple``.
For example:

* Rewrite ``list(list(iterable))`` as ``list(iterable)``
* Rewrite ``list(tuple(iterable))`` as ``list(iterable)``
* Rewrite ``tuple(list(iterable))`` as ``tuple(iterable)``
* Rewrite ``tuple(tuple(iterable))`` as ``tuple(iterable)``
* Rewrite ``set(set(iterable))`` as ``set(iterable)``
* Rewrite ``set(list(iterable))`` as ``set(iterable)``
* Rewrite ``set(tuple(iterable))`` as ``set(iterable)``
* Rewrite ``set(sorted(iterable))`` as ``set(iterable)``
* Rewrite ``set(reversed(iterable))`` as ``set(iterable)``
* Rewrite ``sorted(list(iterable))`` as ``sorted(iterable)``
* Rewrite ``sorted(tuple(iterable))`` as ``sorted(iterable)``
* Rewrite ``sorted(sorted(iterable))`` as ``sorted(iterable)``
* Rewrite ``sorted(reversed(iterable))`` as ``sorted(iterable)``

C415: Unnecessary subscript reversal of iterable within ``<reversed/set/sorted>``\().
-------------------------------------------------------------------------------------

It's unnecessary to reverse the order of an iterable when passing it into one of the listed functions will change the order again.
For example:

* Rewrite ``set(iterable[::-1])`` as ``set(iterable)``
* Rewrite ``sorted(iterable)[::-1]`` as ``sorted(iterable, reverse=True)``
* Rewrite ``reversed(iterable[::-1])`` as ``iterable``

C416: Unnecessary ``<list/set>`` comprehension - rewrite using ``<list/set>``\().
---------------------------------------------------------------------------------

It's unnecessary to use a list comprehension if the elements are unchanged.
The iterable should be wrapped in ``list()`` or ``set()`` instead.
For example:

* Rewrite ``[x for x in iterable]`` as ``list(iterable)``
* Rewrite ``{x for x in iterable}`` as ``set(iterable)``
