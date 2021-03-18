import re
import sys
import textwrap

import pytest

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version


@pytest.fixture
def flake8dir(flake8dir):
    flake8dir.make_setup_cfg(
        textwrap.dedent(
            """\
            [flake8]
            select = C4
            """
        )
    )
    yield flake8dir


def test_version(flake8dir):
    result = flake8dir.run_flake8(["--version"])
    version_regex = r"flake8-comprehensions:( )*" + version("flake8-comprehensions")
    unwrapped = "".join(result.out_lines)
    assert re.search(version_regex, unwrapped)


# C400


def test_C400_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = [x + 1 for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C400_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list(x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C400 Unnecessary generator - rewrite as a list "
        + "comprehension."
    ]


def test_C400_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foobar = list(
            str(x)
            for x
            in range(10)
        )
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:10: C400 Unnecessary generator - rewrite as a list "
        + "comprehension."
    ]


# C401


def test_C401_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = {x + 1 for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C401_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set(x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C401 Unnecessary generator - rewrite as a set "
        + "comprehension."
    ]


def test_C401_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foobar = set(
            str(x) for x
            in range(10)
        )
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:10: C401 Unnecessary generator - rewrite as a set "
        + "comprehension."
    ]


# C402


def test_C402_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = {x: str(x) for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C402_pass_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = ['a=1', 'b=2', 'c=3']
        dict(pair.split('=') for pair in foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C402_pass_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = [('a', 1), ('b', 2), ('c', 3)]
        dict(pair for pair in foo if pair[1] % 2 == 0)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C402_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict((x, str(x)) for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C402 Unnecessary generator - rewrite as a dict "
        + "comprehension."
    ]


def test_C402_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foobar = dict(
            (x, str(x))
            for x
            in range(10)
        )
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:10: C402 Unnecessary generator - rewrite as a dict "
        + "comprehension."
    ]


# C403


def test_C403_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = {x + 1 for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C403_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set([x + 1 for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C403 Unnecessary list comprehension - rewrite as a "
        + "set comprehension."
    ]


# C404


def test_C404_pass_1(flake8dir):
    flake8dir.make_example_py("foo = {x: x for x in range(10)}")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C404_pass_2(flake8dir):
    # Previously a false positive
    flake8dir.make_example_py("foo = dict([x.split('=') for x in ['a=1', 'b=2']])")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C404_fail_1(flake8dir):
    flake8dir.make_example_py("foo = dict([(x, x) for x in range(10)])")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C404 Unnecessary list comprehension - rewrite as a "
        + "dict comprehension."
    ]


# C405


def test_C405_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set(range)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C405_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set([])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C405 Unnecessary list literal - rewrite as a set "
        + "literal."
    ]


def test_C405_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set([1])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C405 Unnecessary list literal - rewrite as a set "
        + "literal."
    ]


def test_C405_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set "
        + "literal."
    ]


def test_C405_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set((1,))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set "
        + "literal."
    ]


# C406


def test_C406_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict(range)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C406_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict([])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C406 Unnecessary list literal - rewrite as a dict "
        + "literal."
    ]


def test_C406_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict([(1, 2)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C406 Unnecessary list literal - rewrite as a dict "
        + "literal."
    ]


def test_C406_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict "
        + "literal."
    ]


def test_C406_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict(((1, 2),))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict "
        + "literal."
    ]


# C408


def test_C408_pass_1(flake8dir):
    flake8dir.make_example_py("()")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_2(flake8dir):
    flake8dir.make_example_py("[]")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_3(flake8dir):
    flake8dir.make_example_py("{}")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_4(flake8dir):
    flake8dir.make_example_py("set()")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_5(flake8dir):
    flake8dir.make_example_py(
        """\
        foo = [('foo', 2)]
        dict(foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_6(flake8dir):
    flake8dir.make_example_py(
        """\
        foo = {}
        dict(bar=1, **foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_7(flake8dir):
    flake8dir.make_example_py(
        """\
        foo = [1, 2]
        list(foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_8(flake8dir):
    flake8dir.make_example_py(
        """\
        foo = [1, 2]
        list(*foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_fail_1(flake8dir):
    flake8dir.make_example_py("tuple()")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C408 Unnecessary tuple call - rewrite as a literal."
    ]


def test_C408_fail_2(flake8dir):
    flake8dir.make_example_py("list()")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C408 Unnecessary list call - rewrite as a literal."
    ]


def test_C408_fail_3(flake8dir):
    flake8dir.make_example_py("dict()")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."
    ]


def test_C408_fail_4(flake8dir):
    flake8dir.make_example_py("dict(a=1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."
    ]


# C409


def test_C409_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple(range)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C409_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple([])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C409 Unnecessary list passed to tuple() - rewrite as "
        + "a tuple literal."
    ]


def test_C409_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple([1, 2])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C409 Unnecessary list passed to tuple() - rewrite as "
        + "a tuple literal."
    ]


def test_C409_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove "
        + "the outer call to tuple()."
    ]


def test_C409_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple((1, 2))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove "
        + "the outer call to tuple()."
    ]


# C410


def test_C410_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list(range)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C410_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list([])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C410 Unnecessary list passed to list() - remove the "
        + "outer call to list()."
    ]


def test_C410_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list([1, 2])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C410 Unnecessary list passed to list() - remove the "
        + "outer call to list()."
    ]


def test_C410_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C410 Unnecessary tuple passed to list() - rewrite as "
        + "a list literal."
    ]


def test_C410_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list((1, 2))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C410 Unnecessary tuple passed to list() - rewrite as "
        + "a list literal."
    ]


# C411


def test_C411_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        [x + 1 for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C411_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        list([x + 1 for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C411 Unnecessary list call - remove the outer call "
        + "to list()."
    ]


# C413


def test_C413_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        sorted([2, 3, 1])
        sorted([2, 3, 1], reverse=True)
        sorted([2, 3, 1], reverse=False)
        sorted([2, 3, 1], reverse=0)
        sorted([2, 3, 1], reverse=1)
        reversed([2, 3, 1])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C413_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        list(sorted([2, 3, 1]))
        reversed(sorted([2, 3, 1]))
        reversed(sorted([2, 3, 1], reverse=False))
        reversed(sorted([2, 3, 1], reverse=True))
        reversed(sorted([2, 3, 1], reverse=0))
        reversed(sorted([2, 3, 1], reverse=1))
        reversed(sorted([2, 3, 1], reverse=bool()))
        reversed(sorted([2, 3, 1], reverse=not True))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C413 Unnecessary list call around sorted().",
        "./example.py:2:1: C413 Unnecessary reversed call around sorted()"
        + " - use sorted(..., reverse=True).",
        "./example.py:3:1: C413 Unnecessary reversed call around sorted()"
        + " - use sorted(..., reverse=True).",
        "./example.py:4:1: C413 Unnecessary reversed call around sorted()"
        + " - use sorted(..., reverse=False).",
        "./example.py:5:1: C413 Unnecessary reversed call around sorted()"
        + " - use sorted(..., reverse=True).",
        "./example.py:6:1: C413 Unnecessary reversed call around sorted()"
        + " - use sorted(..., reverse=False).",
        "./example.py:7:1: C413 Unnecessary reversed call around sorted()"
        + " - toggle reverse argument to sorted().",
        "./example.py:8:1: C413 Unnecessary reversed call around sorted()"
        + " - toggle reverse argument to sorted().",
    ]


# C414


def test_C414_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        a = [2, 3, 1]
        list(set(a))
        tuple(set(a))
        sorted(set(a))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C414_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        a = [2, 3, 1]
        list(list(a))
        list(tuple(a))
        tuple(list(a))
        tuple(tuple(a))
        set(set(a))
        set(list(a))
        set(tuple(a))
        set(sorted(a))
        set(sorted(a, reverse=True))
        set(reversed(a))
        sorted(list(a))
        sorted(tuple(a))
        sorted(sorted(a))
        sorted(sorted(a), reverse=True)
        sorted(sorted(a, reverse=True))
        sorted(sorted(a, reverse=True), reverse=True)
        sorted(reversed(a))
        sorted(reversed(a), reverse=True)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:2:1: C414 Unnecessary list call within list().",
        "./example.py:3:1: C414 Unnecessary tuple call within list().",
        "./example.py:4:1: C414 Unnecessary list call within tuple().",
        "./example.py:5:1: C414 Unnecessary tuple call within tuple().",
        "./example.py:6:1: C414 Unnecessary set call within set().",
        "./example.py:7:1: C414 Unnecessary list call within set().",
        "./example.py:8:1: C414 Unnecessary tuple call within set().",
        "./example.py:9:1: C414 Unnecessary sorted call within set().",
        "./example.py:10:1: C414 Unnecessary sorted call within set().",
        "./example.py:11:1: C414 Unnecessary reversed call within set().",
        "./example.py:12:1: C414 Unnecessary list call within sorted().",
        "./example.py:13:1: C414 Unnecessary tuple call within sorted().",
        "./example.py:14:1: C414 Unnecessary sorted call within sorted().",
        "./example.py:15:1: C414 Unnecessary sorted call within sorted().",
        "./example.py:16:1: C414 Unnecessary sorted call within sorted().",
        "./example.py:17:1: C414 Unnecessary sorted call within sorted().",
        "./example.py:18:1: C414 Unnecessary reversed call within sorted().",
        "./example.py:19:1: C414 Unnecessary reversed call within sorted().",
    ]


# C415


def test_C415_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        set([2, 3, 1][::1])
        sorted([2, 3, 1][::1])
        reversed([2, 3, 1][::1])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C415_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        set([2, 3, 1][::-1])
        sorted([2, 3, 1][::-1])
        sorted([2, 3, 1][::-1], reverse=True)
        reversed([2, 3, 1][::-1])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C415 Unnecessary subscript reversal of iterable "
        + "within set().",
        "./example.py:2:1: C415 Unnecessary subscript reversal of iterable "
        + "within sorted().",
        "./example.py:3:1: C415 Unnecessary subscript reversal of iterable "
        + "within sorted().",
        "./example.py:4:1: C415 Unnecessary subscript reversal of iterable "
        + "within reversed().",
    ]


# C416


def test_C416_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        [str(x) for x in range(5)]
        [x + 1 for x in range(5)]
        [x for x in range(5) if x % 2]
        {str(x) for x in range(5)}
        {x + 1 for x in range(5)}
        {x for x in range(5) if x % 2}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C416_pass_2_async_list(flake8dir):
    flake8dir.make_example_py(
        """\
        async def foo():
            [x async for x in range(5)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C416_pass_3_async_set(flake8dir):
    flake8dir.make_example_py(
        """\
        async def foo():
            return {x async for x in range(5)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C416_pass_4_tuples(flake8dir):
    flake8dir.make_example_py("[(x, y, 1) for x, y in []]")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C416_fail_5_unpacking(flake8dir):
    # We can't assume unpacking came from tuples, so these examples should pass
    flake8dir.make_example_py(
        """
        [(x, y) for x, y in zip('abc', '123')]
        [(x, y) for (x, y) in zip('abc', '123')]
        {(x, y) for x, y in zip('abc', '123')}
        {(x, y) for (x, y) in zip('abc', '123')}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C416_fail_1_list(flake8dir):
    flake8dir.make_example_py("[x for x in range(5)]")
    result = flake8dir.run_flake8()
    # Column offset for list comprehensions was incorrect in Python < 3.8.
    # See https://bugs.python.org/issue31241 for details.
    col_offset = 1 if sys.version_info >= (3, 8) else 2
    assert result.out_lines == [
        "./example.py:1:%d: C416 Unnecessary list comprehension - rewrite using list()."
        % col_offset,
    ]


def test_C416_fail_2_set(flake8dir):
    flake8dir.make_example_py("{x for x in range(5)}")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C416 Unnecessary set comprehension - rewrite using set().",
    ]
