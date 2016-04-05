# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import shutil
import sys
from pathlib import Path
from tempfile import mkdtemp
from textwrap import dedent

from flake8.main import main as flake8_main

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
        tempf.write(dedent(file_contents).strip() + '\n')

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


def test_C100_pass_1():
    errors = run_flake8("""
        foo = [x for x in range(10)]
    """)
    assert errors == []


def test_C100_fail_1():
    errors = run_flake8("""
        foo = list(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C100 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C100_fail_2():
    errors = run_flake8("""
        foobar = list(
            str(x)
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C100 Unnecessary generator - rewrite as a list comprehension.',
    ]


def test_C101_pass_1():
    errors = run_flake8("""
        foo = {x for x in range(10)}
    """)
    assert errors == []


def test_C101_fail_1():
    errors = run_flake8("""
        foo = set(x for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C101 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C101_fail_2():
    errors = run_flake8("""
        foobar = set(
            str(x) for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C101 Unnecessary generator - rewrite as a set comprehension.',
    ]


def test_C102_pass_1():
    errors = run_flake8("""
        foo = {x: str(x) for x in range(10)}
    """)
    assert errors == []


def test_C102_fail_1():
    errors = run_flake8("""
        foo = dict((x, str(x)) for x in range(10))
    """)
    assert errors == [
        'example.py:1:7: C102 Unnecessary generator - rewrite as a dict comprehension.',
    ]


def test_C102_fail_2():
    errors = run_flake8("""
        foobar = dict(
            (x, str(x))
            for x
            in range(10)
        )
    """)
    assert errors == [
        'example.py:1:10: C102 Unnecessary generator - rewrite as a dict comprehension.',
    ]
