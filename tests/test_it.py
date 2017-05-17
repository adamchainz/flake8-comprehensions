# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp
from textwrap import dedent

from flake8.main.cli import main as flake8_main

from .utils import captured_stdout

MODULE_DIR = Path(__file__).parent.resolve()
TMP_DIR = None


def setup_module(module):
    global TMP_DIR
    TMP_DIR = Path(mkdtemp())


def teardown_module(module):
    shutil.rmtree(str(TMP_DIR))


def run_flake8(file_contents):
    with open(str(TMP_DIR / "example.py"), 'w') as tempf:
        tempf.write(dedent(file_contents.lstrip('\n')).strip() + '\n')

    orig_dir = os.getcwd()
    os.chdir(str(TMP_DIR))
    orig_args = sys.argv
    try:
        # Can't pass args to flake8 but can set to sys.argv
        sys.argv = [
            'flake8',
            '--jobs', '1',
            '--exit-zero',
            'example.py',
        ]

        # Run it
        with captured_stdout() as stdout:
            flake8_main()
        out = stdout.getvalue().strip()
        lines = out.split('\n')
        if lines[-1] == '':
            lines = lines[:-1]
        return lines
    finally:
        sys.argv = orig_args
        os.chdir(orig_dir)


def test_C400_pass_1():
    errors = run_flake8("""
        foo = [x for x in range(10)]
    """)
    assert errors == []


def test_C400_fail_1():
    errors = run_flake8("""
        foo = list(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C400 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C400_fail_2():
    errors = run_flake8("""
        foobar = list(
            str(x)
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C400 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C401_pass_1():
    errors = run_flake8("""
        foo = {x for x in range(10)}
    """)
    assert errors == []


def test_C401_fail_1():
    errors = run_flake8("""
        foo = set(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C401 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C401_fail_2():
    errors = run_flake8("""
        foobar = set(
            str(x) for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C401 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C402_pass_1():
    errors = run_flake8("""
        foo = {x: str(x) for x in range(10)}
    """)
    assert errors == []


def test_C402_pass_2():
    errors = run_flake8("""
        foo = ['a=1', 'b=2', 'c=3']
        dict(pair.split('=') for pair in foo)
    """)
    assert errors == []


def test_C402_pass_3():
    errors = run_flake8("""
        foo = [('a', 1), ('b', 2), ('c', 3)]
        dict(pair for pair in foo if pair[1] % 2 == 0)
    """)
    assert errors == []


def test_C402_fail_1():
    errors = run_flake8("""
        foo = dict((x, str(x)) for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C402 Unnecessary generator - rewrite as a dict comprehension.',
    ]


def test_C402_fail_2():
    errors = run_flake8("""
        foobar = dict(
            (x, str(x))
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C402 Unnecessary generator - rewrite as a dict comprehension.',
    ]


def test_C403_pass_1():
    errors = run_flake8("""
        foo = {x for x in range(10)}
    """)
    assert errors == []


def test_C403_fail_1():
    errors = run_flake8("""
        foo = set([x for x in range(10)])
    """)
    assert errors == [
        'example.py:1:7: C403 Unnecessary list comprehension - rewrite as a set comprehension.',
    ]


def test_C404_pass_1():
    errors = run_flake8("""
        foo = {x: x for x in range(10)}
    """)
    assert errors == []


def test_C404_fail_1():
    errors = run_flake8("""
        foo = dict([(x, x) for x in range(10)])
    """)
    assert errors == [
        'example.py:1:7: C404 Unnecessary list comprehension - rewrite as a dict comprehension.',
    ]


def test_C405_pass_1():
    errors = run_flake8("""
        foo = set(range)
    """)
    assert errors == []


def test_C405_fail_1():
    errors = run_flake8("""
        foo = set([])
    """)
    assert errors == [
        'example.py:1:7: C405 Unnecessary list literal - rewrite as a set literal.',
    ]


def test_C405_fail_2():
    errors = run_flake8("""
        foo = set([1])
    """)
    assert errors == [
        'example.py:1:7: C405 Unnecessary list literal - rewrite as a set literal.',
    ]


def test_C405_fail_3():
    errors = run_flake8("""
        foo = set(())
    """)
    assert errors == [
        'example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set literal.',
    ]


def test_C405_fail_4():
    errors = run_flake8("""
        foo = set((1,))
    """)
    assert errors == [
        'example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set literal.',
    ]


def test_C406_pass_1():
    errors = run_flake8("""
        foo = dict(range)
    """)
    assert errors == []


def test_C406_fail_1():
    errors = run_flake8("""
        foo = dict([])
    """)
    assert errors == [
        'example.py:1:7: C406 Unnecessary list literal - rewrite as a dict literal.',
    ]


def test_C406_fail_2():
    errors = run_flake8("""
        foo = dict([(1, 2)])
    """)
    assert errors == [
        'example.py:1:7: C406 Unnecessary list literal - rewrite as a dict literal.',
    ]


def test_C406_fail_3():
    errors = run_flake8("""
        foo = dict(())
    """)
    assert errors == [
        'example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict literal.',
    ]


def test_C406_fail_4():
    errors = run_flake8("""
        foo = dict(((1, 2),))
    """)
    assert errors == [
        'example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict literal.',
    ]


def test_C407_sum_pass_1():
    errors = run_flake8("""
        foo = sum(x for x in range(10))
    """)
    assert errors == []


def test_C407_sum_fail_1():
    errors = run_flake8("""
        foo = sum([x for x in range(10)])
    """)
    assert errors == [
        "example.py:1:7: C407 Unnecessary list comprehension - 'sum' can take a generator.",
    ]


def test_C407_max_fail_1():
    errors = run_flake8("""
        foo = max([x for x in range(10)])
    """)
    assert errors == [
        "example.py:1:7: C407 Unnecessary list comprehension - 'max' can take a generator.",
    ]


def test_C407_tuple_pass_1():
    errors = run_flake8("""
        foo = ()
    """)
    assert errors == []


def test_C407_tuple_pass_2():
    errors = run_flake8("""
        foo = tuple(x for x in range(10))
    """)
    assert errors == []


def test_C407_tuple_fail_1():
    errors = run_flake8("""
        foo = tuple([x for x in range(10)])
    """)
    assert errors == [
        "example.py:1:7: C407 Unnecessary list comprehension - 'tuple' can take a generator.",
    ]


def test_it_does_not_crash_on_attribute_functions():
    errors = run_flake8("""
        import foo
        bar = foo.baz(x for x in range(10))
    """)
    assert errors == []


def test_C408_pass_1():
    errors = run_flake8('()')
    assert errors == []


def test_C408_pass_2():
    errors = run_flake8('[]')
    assert errors == []


def test_C408_pass_3():
    errors = run_flake8('{}')
    assert errors == []


def test_C408_pass_4():
    errors = run_flake8('set()')
    assert errors == []


def test_C408_pass_5():
    errors = run_flake8('''\
        foo = {}
        dict(bar=1, **foo)
    ''')
    assert errors == []


def test_C408_pass_6():
    errors = run_flake8('''\
        foo = [1, 2]
        list(*foo)
    ''')
    assert errors == []


def test_C408_fail_1():
    errors = run_flake8('tuple()')
    assert errors == [
        "example.py:1:1: C408 Unnecessary tuple call - rewrite as a literal."
    ]


def test_C408_fail_2():
    errors = run_flake8('list()')
    assert errors == [
        "example.py:1:1: C408 Unnecessary list call - rewrite as a literal."
    ]


def test_C408_fail_3():
    errors = run_flake8('dict()')
    assert errors == [
        "example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."
    ]


def test_C408_fail_4():
    errors = run_flake8('dict(a=1)')
    assert errors == [
        "example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."
    ]


def test_C409_pass_1():
    errors = run_flake8("""
        foo = tuple(range)
    """)
    assert errors == []


def test_C409_fail_1():
    errors = run_flake8("""
        foo = tuple([])
    """)
    assert errors == [
        'example.py:1:7: C409 Unnecessary list passed to tuple() - rewrite as a tuple literal.',
    ]


def test_C409_fail_2():
    errors = run_flake8("""
        foo = tuple([1, 2])
    """)
    assert errors == [
        'example.py:1:7: C409 Unnecessary list passed to tuple() - rewrite as a tuple literal.',
    ]


def test_C409_fail_3():
    errors = run_flake8("""
        foo = tuple(())
    """)
    assert errors == [
        'example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove the outer call to tuple().',
    ]


def test_C409_fail_4():
    errors = run_flake8("""
        foo = tuple((1, 2))
    """)
    assert errors == [
        'example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove the outer call to tuple().',
    ]


def test_C410_pass_1():
    errors = run_flake8("""
        foo = list(range)
    """)
    assert errors == []


def test_C410_fail_1():
    errors = run_flake8("""
        foo = list([])
    """)
    assert errors == [
        'example.py:1:7: C410 Unnecessary list passed to list() - remove the outer call to list().',
    ]


def test_C410_fail_2():
    errors = run_flake8("""
        foo = list([1, 2])
    """)
    assert errors == [
        'example.py:1:7: C410 Unnecessary list passed to list() - remove the outer call to list().',
    ]


def test_C410_fail_3():
    errors = run_flake8("""
        foo = list(())
    """)
    assert errors == [
        'example.py:1:7: C410 Unnecessary tuple passed to list() - rewrite as a list literal.',
    ]


def test_C410_fail_4():
    errors = run_flake8("""
        foo = list((1, 2))
    """)
    assert errors == [
        'example.py:1:7: C410 Unnecessary tuple passed to list() - rewrite as a list literal.',
    ]


def test_C411_pass_1():
    errors = run_flake8("""
        [x for x in range(10)]
    """)
    assert errors == []


def test_C411_fail_1():
    errors = run_flake8("""
        list([x for x in range(10)])
    """)
    assert errors == [
        'example.py:1:1: C411 Unnecessary list call - remove the outer call to list().',
    ]
