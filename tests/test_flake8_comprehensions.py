from __future__ import annotations

import re
import sys
from textwrap import dedent

import pytest

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version


@pytest.fixture
def flake8_path(flake8_path):
    (flake8_path / "setup.cfg").write_text(
        dedent(
            """\
            [flake8]
            select = C4
            """
        )
    )
    yield flake8_path


def test_version(flake8_path):
    result = flake8_path.run_flake8(["--version"])
    version_regex = r"flake8-comprehensions:( )*" + version("flake8-comprehensions")
    unwrapped = "".join(result.out_lines)
    assert re.search(version_regex, unwrapped)


@pytest.mark.parametrize(
    "code",
    [
        "foo = [x + 1 for x in range(10)]",
    ],
)
def test_C400_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = list(x + 1 for x in range(10))",
            [
                "./example.py:1:7: C400 Unnecessary generator - rewrite as a list "
                + "comprehension."
            ],
        ),
        (
            """\
            foobar = list(
                str(x)
                for x
                in range(10)
            )
            """,
            [
                "./example.py:1:10: C400 Unnecessary generator - rewrite as a list "
                + "comprehension."
            ],
        ),
    ],
)
def test_C400_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = {x + 1 for x in range(10)}",
    ],
)
def test_C401_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = set(x + 1 for x in range(10))",
            [
                "./example.py:1:7: C401 Unnecessary generator - rewrite as a set "
                + "comprehension."
            ],
        ),
        (
            """\
            foobar = set(
                str(x) for x
                in range(10)
            )
            """,
            [
                "./example.py:1:10: C401 Unnecessary generator - rewrite as a set "
                + "comprehension."
            ],
        ),
    ],
)
def test_C401_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = {x: str(x) for x in range(10)}",
        """\
        foo = ['a=1', 'b=2', 'c=3']
        dict(pair.split('=') for pair in foo)
        """,
        """\
        foo = [('a', 1), ('b', 2), ('c', 3)]
        dict(pair for pair in foo if pair[1] % 2 == 0)
        """,
        # Previously a false positive:
        "dict(((x, str(x)) for x in range(10)), c=1)",
    ],
)
def test_C402_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = dict((x, str(x)) for x in range(10))",
            [
                "./example.py:1:7: C402 Unnecessary generator - rewrite as a dict "
                + "comprehension."
            ],
        ),
        (
            """\
            foobar = dict(
                (x, str(x))
                for x
                in range(10)
            )
            """,
            [
                "./example.py:1:10: C402 Unnecessary generator - rewrite as a dict "
                + "comprehension."
            ],
        ),
    ],
)
def test_C402_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = {x + 1 for x in range(10)}",
    ],
)
def test_C403_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = set([x + 1 for x in range(10)])",
            [
                "./example.py:1:7: C403 Unnecessary list comprehension - rewrite as a "
                + "set comprehension."
            ],
        ),
    ],
)
def test_C403_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = {x: x for x in range(10)}",
        # Previously a false positive:
        "foo = dict([x.split('=') for x in ['a=1', 'b=2']])",
        # Previously a false positive:
        "dict([(x, x) for x in range(10)], y=2)",
    ],
)
def test_C404_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = dict([(x, x) for x in range(10)])",
            [
                "./example.py:1:7: C404 Unnecessary list comprehension - rewrite as a "
                + "dict comprehension."
            ],
        ),
    ],
)
def test_C404_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = set(range)",
    ],
)
def test_C405_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = set([])",
            [
                "./example.py:1:7: C405 Unnecessary list literal - rewrite as a set "
                + "literal."
            ],
        ),
        (
            "foo = set([1])",
            [
                "./example.py:1:7: C405 Unnecessary list literal - rewrite as a set "
                + "literal."
            ],
        ),
        (
            "foo = set(())",
            [
                "./example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set "
                + "literal."
            ],
        ),
        (
            "foo = set((1,))",
            [
                "./example.py:1:7: C405 Unnecessary tuple literal - rewrite as a set "
                + "literal."
            ],
        ),
    ],
)
def test_C405_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = dict(range)",
    ],
)
def test_C406_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = dict([])",
            [
                "./example.py:1:7: C406 Unnecessary list literal - rewrite as a dict "
                + "literal."
            ],
        ),
        (
            "foo = dict([(1, 2)])",
            [
                "./example.py:1:7: C406 Unnecessary list literal - rewrite as a dict "
                + "literal."
            ],
        ),
        (
            "foo = dict(())",
            [
                "./example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict "
                + "literal."
            ],
        ),
        (
            "foo = dict(((1, 2),))",
            [
                "./example.py:1:7: C406 Unnecessary tuple literal - rewrite as a dict "
                + "literal."
            ],
        ),
    ],
)
def test_C406_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "()",
        "[]",
        "{}",
        "set()",
        """\
        foo = [('foo', 2)]
        dict(foo)
        """,
        """\
        foo = {}
        dict(bar=1, **foo)
        """,
        """\
        foo = [1, 2]
        list(foo)
        """,
        """\
        foo = [1, 2]
        list(*foo)
        """,
    ],
)
def test_C408_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "tuple()",
            ["./example.py:1:1: C408 Unnecessary tuple call - rewrite as a literal."],
        ),
        (
            "list()",
            ["./example.py:1:1: C408 Unnecessary list call - rewrite as a literal."],
        ),
        (
            "dict()",
            ["./example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."],
        ),
        (
            "dict(a=1)",
            ["./example.py:1:1: C408 Unnecessary dict call - rewrite as a literal."],
        ),
    ],
)
def test_C408_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = tuple(range)",
    ],
)
def test_C409_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = tuple([])",
            [
                "./example.py:1:7: C409 Unnecessary list passed to tuple() - "
                + "rewrite as a tuple literal."
            ],
        ),
        (
            "foo = tuple([1, 2])",
            [
                "./example.py:1:7: C409 Unnecessary list passed to tuple() - "
                + "rewrite as a tuple literal."
            ],
        ),
        (
            "foo = tuple(())",
            [
                "./example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove "
                + "the outer call to tuple()."
            ],
        ),
        (
            "foo = tuple((1, 2))",
            [
                "./example.py:1:7: C409 Unnecessary tuple passed to tuple() - remove "
                + "the outer call to tuple()."
            ],
        ),
    ],
)
def test_C409_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "foo = list(range)",
    ],
)
def test_C410_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "foo = list([])",
            [
                "./example.py:1:7: C410 Unnecessary list passed to list() - remove the "
                + "outer call to list()."
            ],
        ),
        (
            "foo = list([1, 2])",
            [
                "./example.py:1:7: C410 Unnecessary list passed to list() - remove the "
                + "outer call to list()."
            ],
        ),
        (
            "foo = list(())",
            [
                "./example.py:1:7: C410 Unnecessary tuple passed to list() - "
                + "rewrite as a list literal."
            ],
        ),
        (
            "foo = list((1, 2))",
            [
                "./example.py:1:7: C410 Unnecessary tuple passed to list() - "
                + "rewrite as a list literal."
            ],
        ),
    ],
)
def test_C410_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "[x + 1 for x in range(10)]",
    ],
)
def test_C411_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "list([x + 1 for x in range(10)])",
            [
                "./example.py:1:1: C411 Unnecessary list call - remove the outer call "
                + "to list()."
            ],
        ),
    ],
)
def test_C411_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "sorted([2, 3, 1])",
        "sorted([2, 3, 1], reverse=True)",
        "sorted([2, 3, 1], reverse=False)",
        "sorted([2, 3, 1], reverse=0)",
        "sorted([2, 3, 1], reverse=1)",
        "reversed([2, 3, 1])",
    ],
)
def test_C413_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "list(sorted([2, 3, 1]))",
            ["./example.py:1:1: C413 Unnecessary list call around sorted()."],
        ),
        (
            "reversed(sorted([2, 3, 1]))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - use sorted(..., reverse=True)."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=False))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - use sorted(..., reverse=True)."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=True))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - use sorted(..., reverse=False)."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=0))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - use sorted(..., reverse=True)."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=1))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - use sorted(..., reverse=False)."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=bool()))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - toggle reverse argument to sorted()."
            ],
        ),
        (
            "reversed(sorted([2, 3, 1], reverse=not True))",
            [
                "./example.py:1:1: C413 Unnecessary reversed call around sorted()"
                + " - toggle reverse argument to sorted()."
            ],
        ),
    ],
)
def test_C413_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "list(set(a))",
        "tuple(set(a))",
        "sorted(set(a))",
    ],
)
def test_C414_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "list(list(a))",
            ["./example.py:1:1: C414 Unnecessary list call within list()."],
        ),
        (
            "list(tuple(a))",
            ["./example.py:1:1: C414 Unnecessary tuple call within list()."],
        ),
        (
            "tuple(list(a))",
            ["./example.py:1:1: C414 Unnecessary list call within tuple()."],
        ),
        (
            "tuple(tuple(a))",
            ["./example.py:1:1: C414 Unnecessary tuple call within tuple()."],
        ),
        ("set(set(a))", ["./example.py:1:1: C414 Unnecessary set call within set()."]),
        (
            "set(list(a))",
            ["./example.py:1:1: C414 Unnecessary list call within set()."],
        ),
        (
            "set(tuple(a))",
            ["./example.py:1:1: C414 Unnecessary tuple call within set()."],
        ),
        (
            "set(sorted(a))",
            ["./example.py:1:1: C414 Unnecessary sorted call within set()."],
        ),
        (
            "set(sorted(a, reverse=True))",
            ["./example.py:1:1: C414 Unnecessary sorted call within set()."],
        ),
        (
            "set(reversed(a))",
            ["./example.py:1:1: C414 Unnecessary reversed call within set()."],
        ),
        (
            "sorted(list(a))",
            ["./example.py:1:1: C414 Unnecessary list call within sorted()."],
        ),
        (
            "sorted(tuple(a))",
            ["./example.py:1:1: C414 Unnecessary tuple call within sorted()."],
        ),
        (
            "sorted(sorted(a))",
            ["./example.py:1:1: C414 Unnecessary sorted call within sorted()."],
        ),
        (
            "sorted(sorted(a), reverse=True)",
            ["./example.py:1:1: C414 Unnecessary sorted call within sorted()."],
        ),
        (
            "sorted(sorted(a, reverse=True))",
            ["./example.py:1:1: C414 Unnecessary sorted call within sorted()."],
        ),
        (
            "sorted(sorted(a, reverse=True), reverse=True)",
            ["./example.py:1:1: C414 Unnecessary sorted call within sorted()."],
        ),
        (
            "sorted(reversed(a))",
            ["./example.py:1:1: C414 Unnecessary reversed call within sorted()."],
        ),
        (
            "sorted(reversed(a), reverse=True)",
            ["./example.py:1:1: C414 Unnecessary reversed call within sorted()."],
        ),
    ],
)
def test_C414_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "set([2, 3, 1][::1])",
        "sorted([2, 3, 1][::1])",
        "reversed([2, 3, 1][::1])",
    ],
)
def test_C415_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "set([2, 3, 1][::-1])",
            [
                "./example.py:1:1: C415 Unnecessary subscript reversal of iterable "
                + "within set()."
            ],
        ),
        (
            "sorted([2, 3, 1][::-1])",
            [
                "./example.py:1:1: C415 Unnecessary subscript reversal of iterable "
                + "within sorted()."
            ],
        ),
        (
            "sorted([2, 3, 1][::-1], reverse=True)",
            [
                "./example.py:1:1: C415 Unnecessary subscript reversal of iterable "
                + "within sorted()."
            ],
        ),
        (
            "reversed([2, 3, 1][::-1])",
            [
                "./example.py:1:1: C415 Unnecessary subscript reversal of iterable "
                + "within reversed()."
            ],
        ),
    ],
)
def test_C415_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "{x, y for x, y, z in zip('abc', '123', 'def')}",
        "{y: x for x, y in zip('abc', '123')}",
        "{x: y for x, (y,) in zip('a', ('1',))}",
        "{x: z for x, (y,), z in zip('a', ('1',), 'b')}",
        "[str(x) for x in range(5)]",
        "[x + 1 for x in range(5)]",
        "[x for x in range(5) if x % 2]",
        "{str(x) for x in range(5)}",
        "{x + 1 for x in range(5)}",
        "{x for x in range(5) if x % 2}",
        """\
        async def foo():
            [x async for x in range(5)]
        """,
        """\
        async def foo():
            return {x async for x in range(5)}
        """,
        "[(x, y, 1) for x, y in []]",
        # We can't assume unpacking came from tuples:
        "[(x, y) for x, y in zip('abc', '123')]",
        "[(x, y) for (x, y) in zip('abc', '123')]",
        "{(x, y) for x, y in zip('abc', '123')}",
        "{(x, y) for (x, y) in zip('abc', '123')}",
    ],
)
def test_C416_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


# Column offset for list comprehensions was incorrect in Python < 3.8.
# See https://bugs.python.org/issue31241 for details.
if sys.version_info >= (3, 8):
    list_comp_col_offset = 0
else:
    list_comp_col_offset = 1


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "{x: y for x, y in zip(range(5), range(5))}",
            [
                "./example.py:1:1: C416 Unnecessary dict comprehension - "
                + "rewrite using dict().",
            ],
        ),
        (
            "{x: y for (x, y) in zip(range(5), range(5))}",
            [
                "./example.py:1:1: C416 Unnecessary dict comprehension - "
                + "rewrite using dict().",
            ],
        ),
        (
            "[x for x in range(5)]",
            [
                f"./example.py:1:{1 + list_comp_col_offset}: C416 Unnecessary "
                + "list comprehension - rewrite using list()."
            ],
        ),
        (
            "{x for x in range(5)}",
            [
                "./example.py:1:1: C416 Unnecessary set comprehension - "
                + "rewrite using set().",
            ],
        ),
    ],
)
def test_C416_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures


@pytest.mark.parametrize(
    "code",
    [
        "map()",
        "map(str, numbers)",
        "list(map())",
        "list(map(str, numbers))",
        "set(map(f, items))",
        "dict(map(enumerate, values))",
        "dict(map(lambda v: data[v], values))",
    ],
)
def test_C417_pass(code, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == []


@pytest.mark.parametrize(
    "code,failures",
    [
        (
            "map(lambda x: x * 2, iterable)",
            [
                "./example.py:1:1: C417 Unnecessary use of map - "
                + "use a generator expression instead.",
            ],
        ),
        (
            "list(map(lambda x: x * 2, iterable))",
            [
                "./example.py:1:1: C417 Unnecessary use of map - "
                + "use a list comprehension instead.",
            ],
        ),
        (
            "set(map(lambda num: num % 2 == 0, nums))",
            [
                "./example.py:1:1: C417 Unnecessary use of map - "
                + "use a set comprehension instead.",
            ],
        ),
        (
            "dict(map(lambda v: (v, v ** 2), values))",
            [
                "./example.py:1:1: C417 Unnecessary use of map - "
                "use a dict comprehension instead.",
            ],
        ),
    ],
)
def test_C417_fail(code, failures, flake8_path):
    (flake8_path / "example.py").write_text(dedent(code))
    result = flake8_path.run_flake8()
    assert result.out_lines == failures
