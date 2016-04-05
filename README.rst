=====================
Flake8 Comprehensions
=====================

.. image:: https://img.shields.io/pypi/v/flake8-comprehensions.svg
        :target: https://pypi.python.org/pypi/flake8-comprehensions

.. image:: https://img.shields.io/travis/adamchainz/flake8-comprehensions.svg
        :target: https://travis-ci.org/adamchainz/flake8-comprehensions

A `flake8 <https://flake8.readthedocs.org/en/latest/index.html>`_ plugin that
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

C400: Unnecessary generator
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Complains about unnecessary use of a generator when a list/set/dict
comprehension would do:

For example, an unnecessary usage of ``list()`` plus a generator, instead of a
list comprehension:

* ``list(f(x) for x in foo)`` -> ``[f(x) for x in foo]``

This triggers a message like:

.. code-block:: sh

    $ flake8 file.py
    file.py:1:1: C400 Unnecessary generator - rewrite as a list comprehension.

This works similarly for ``set()`` and ``dict()`` with generators instead of
their respective comprehensions.
