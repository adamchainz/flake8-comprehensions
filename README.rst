=====================
flake8-comprehensions
=====================

.. image:: https://img.shields.io/pypi/v/flake8-comprehensions.svg
        :target: https://pypi.org/project/flake8-comprehensions/

.. image:: https://img.shields.io/travis/adamchainz/flake8-comprehensions.svg
        :target: https://travis-ci.org/adamchainz/flake8-comprehensions

A `flake8 <https://flake8.readthedocs.io/en/latest/index.html>`_ plugin that
helps you write better list/set/dict comprehensions.

Installation
------------

Install from ``pip`` with:

.. code-block:: sh

     pip install flake8-comprehensions

Python 3.4+ supported.

When installed it will automatically be run as part of ``flake8``; you can
check it is being picked up with:

.. code-block:: sh

    $ flake8 --version
    2.4.1 (pep8: 1.7.0, pyflakes: 0.8.1, flake8-comprehensions: 1.0.0, mccabe: 0.3.1) CPython 2.7.11 on Darwin


Rules
-----

==== ====
Code Rule
==== ====
C400 Unnecessary generator - rewrite as a list comprehension.
C401 Unnecessary generator - rewrite as a set comprehension.
C402 Unnecessary generator - rewrite as a dict comprehension.
C403 Unnecessary list comprehension - rewrite as a set comprehension.
C404 Unnecessary list comprehension - rewrite as a dict comprehension.
C405 Unnecessary (list/tuple) literal - rewrite as a set literal.
C406 Unnecessary (list/tuple) literal - rewrite as a dict literal.
C407 Unnecessary list comprehension - '<builtin>' can take a generator.
C408 Unnecessary (dict/list/tuple) call - rewrite as a literal.
C409 Unnecessary (list/tuple) passed to tuple() - (remove the outer call to tuple()/rewrite as a tuple literal).
C410 Unnecessary (list/tuple) passed to list() - (remove the outer call to list()/rewrite as a list literal).
C411 Unnecessary list call - remove the outer call to list().
==== ====

Examples
--------

C400-402: Unnecessary generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use ``list``, ``set``, or ``dict`` around a generator
expression, since there are equivalent comprehensions for these types. For
example:

* Rewrite ``list(f(x) for x in foo)`` as ``[f(x) for x in foo]``
* Rewrite ``set(f(x) for x in foo)`` as ``{f(x) for x in foo}``
* Rewrite ``dict((x, f(x)) for x in foo)`` as ``{x: f(x) for x in foo}``

C403-404: Unnecessary list comprehension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use a list comprehension inside a call to ``set`` or
``dict``, since there are equivalent comprehensions for these types. For
example:

* Rewrite ``set([f(x) for x in foo])`` as ``{f(x) for x in foo}``
* Rewrite ``dict([(x, f(x)) for x in foo])`` as ``{x: f(x) for x in foo}``

C405-406,C409-410: Unnecessary list/tuple literal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use a list or tuple literal within a call to ``tuple``,
``list``, ``set``, or ``dict`` since there is literal syntax for these types.
For example:

* Rewrite ``tuple([1, 2])`` or ``tuple((1, 2))`` as ``(1, 2)``
* Rewrite ``tuple([])`` as ``()``
* Rewrite ``list([1, 2])`` or ``list((1, 2))`` as ``[1, 2]``
* Rewrite ``list([])`` is better as ``[]``
* Rewrite ``set([1, 2])`` or ``set((1, 2))`` as ``{1, 2}``
* Rewrite ``set([])`` as ``set()``
* Rewrite ``dict([(1, 2)])`` or ``dict(((1, 2),))`` as ``{1: 2}``
* Rewrite ``dict([])`` as ``{}``

C407: Unnecessary list comprehension - '<builtin>' can take a generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to pass a list comprehension to some builtins that can take
generators instead. For example:

* Rewrite ``sum([x ** 2 for x in range(10)])`` as
  ``sum(x ** 2 for x in range(10))``
* Rewrite ``all([foo.bar for foo in foos])`` as
  ``all(foo.bar for foo in foos)``

The list of builtins that are checked for are:

* ``all``
* ``any``
* ``enumerate``
* ``frozenset``
* ``max``
* ``min``
* ``sorted``
* ``sum``
* ``tuple``

C408: Unnecessary (dict/list/tuple) call - rewrite as a literal.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's slower to call e.g. ``dict()`` than using the empty literal, because the
name ``dict`` must be looked up in the global scope in case it has been
rebound. Same for the other two basic types here. For example:

* Rewrite ``dict()`` as ``{}``
* Rewrite ``list()`` as ``[]``
* Rewrite ``tuple()`` as ``()``

C411: Unnecessary list call - remove the outer call to list().
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use a ``list`` around list comprehension, since it is
equivalent without it. For example:

* Rewrite ``list([f(x) for x in foo])`` as ``[f(x) for x in foo]``
