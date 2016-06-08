=====================
flake8-comprehensions
=====================

.. image:: https://img.shields.io/pypi/v/flake8-comprehensions.svg
        :target: https://pypi.python.org/pypi/flake8-comprehensions

.. image:: https://img.shields.io/travis/adamchainz/flake8-comprehensions.svg
        :target: https://travis-ci.org/adamchainz/flake8-comprehensions

A `flake8 <https://flake8.readthedocs.io/en/latest/index.html>`_ plugin that
helps you write better list/set/dict comprehensions.

* Free software: ISC license

Installation
------------

Install from ``pip`` with:

.. code-block:: sh

     pip install flake8-comprehensions

It will then automatically be run as part of ``flake8``; you can check it has
been picked up with:

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
C405 Unnecessary list literal - rewrite as a set literal.
C406 Unnecessary list literal - rewrite as a dict literal.
==== ====

Examples
--------

C400-402: Unnecessary generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use ``list``, ``set``, or ``dict`` around a generator
expression, since there are equivalent comprehensions for these types. For
example:

* ``list(f(x) for x in foo)`` is better as ``[f(x) for x in foo]``
* ``set(f(x) for x in foo)`` is better as ``{f(x) for x in foo}``
* ``dict((x, f(x)) for x in foo)`` is better as ``{x: f(x) for x in foo}``

C403-404: Unnecessary list comprehension
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use a list comprehension inside a call to ``set`` or
``dict``, since there are equivalent comprehensions for these types. For
example:

* ``set([f(x) for x in foo])`` is better as ``{f(x) for x in foo}``
* ``dict([(x, f(x)) for x in foo])`` is better as ``{x: f(x) for x in foo}``

C405-406: Unnecessary list literal
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's unnecessary to use a list literal within a call to ``set`` or ``dict``
since there is literal syntax for these types. For example:

* ``set([1, 2])`` is better as ``{1, 2}``
* ``set([])`` is better as ``set()``
* ``dict([])`` is better as ``{}``
* ``dict([(1, 2)])`` is better as ``{1: 2}``
