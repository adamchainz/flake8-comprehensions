import os
import sys

import pytest

from flake8_comprehensions import ComprehensionChecker

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version


python_3_6_plus = pytest.mark.skipif(sys.version_info < (3, 6), reason="Python 3.6+")


def test_version(flake8dir):
    result = flake8dir.run_flake8(["--version"])
    version_string = "flake8-comprehensions: " + version("flake8-comprehensions")
    assert version_string in result.out_lines[0]


def make_message(code, line, col, suffix=None, **kwds):
    msg = ComprehensionChecker.messages[code]
    if suffix is not None:
        msg = msg.replace("{suffix}", ComprehensionChecker.suffixes.get(suffix, ""))
    if kwds:
        msg = msg.format(**kwds)
    return ".{}example.py:{}:{}: {}".format(os.path.sep, line, col, msg)


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
    assert result.out_lines == [make_message("C400", 1, 7)]


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
    assert result.out_lines == [make_message("C400", 1, 10)]


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
    assert result.out_lines == [make_message("C401", 1, 7)]


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
    assert result.out_lines == [make_message("C401", 1, 10)]


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
    assert result.out_lines == [make_message("C402", 1, 7)]


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
    assert result.out_lines == [make_message("C402", 1, 10)]


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
    assert result.out_lines == [make_message("C403", 1, 7)]


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
    assert result.out_lines == [make_message("C404", 1, 7)]


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
        make_message("C405", 1, 7, type="list", func="set", suffix="rw")
    ]


def test_C405_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set([1])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C405", 1, 7, type="list", func="set", suffix="rw")
    ]


def test_C405_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C405", 1, 7, type="tuple", func="set", suffix="rw")
    ]


def test_C405_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set((1,))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C405", 1, 7, type="tuple", func="set", suffix="rw")
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
        make_message("C406", 1, 7, type="list", func="dict", suffix="rw")
    ]


def test_C406_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict([(1, 2)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C406", 1, 7, type="list", func="dict", suffix="rw")
    ]


def test_C406_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C406", 1, 7, type="tuple", func="dict", suffix="rw")
    ]


def test_C406_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict(((1, 2),))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C406", 1, 7, type="tuple", func="dict", suffix="rw")
    ]


# C407


def test_C407_sum_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = sum(x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_sum_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = sum([x + 1 for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 7, func="sum")]


def test_C407_max_pass_1(flake8dir):
    flake8dir.make_example_py("max(x + 1 for x in range(10))")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_pass_2(flake8dir):
    flake8dir.make_example_py("max((x + 1 for x in range(10)), key=lambda x: x * 2)")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_pass_3(flake8dir):
    flake8dir.make_example_py(
        "max((x + 1 for x in range(10)), default=1, key=lambda x: x * 2)"
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_fail_1(flake8dir):
    flake8dir.make_example_py("max([x + 1 for x in range(10)])")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 1, func="max")]


def test_C407_max_fail_2(flake8dir):
    flake8dir.make_example_py("max([x + 1 for x in range(10)], default=1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 1, func="max")]


def test_C407_enumerate_pass_1(flake8dir):
    flake8dir.make_example_py("enumerate(1 for i in range(10))")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_enumerate_pass_2(flake8dir):
    flake8dir.make_example_py("enumerate((1 for i in range(10)), 1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_enumerate_pass_3(flake8dir):
    flake8dir.make_example_py("enumerate((1 for i in range(10)), start=1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_enumerate_fail_1(flake8dir):
    flake8dir.make_example_py("enumerate([x + 1 for x in range(10)])")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 1, func="enumerate")]


def test_C407_enumerate_fail_2(flake8dir):
    flake8dir.make_example_py("enumerate([x + 1 for x in range(10)], 1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 1, func="enumerate")]


def test_C407_tuple_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = ()
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_tuple_pass_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple(x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_tuple_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple([x + 1 for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C407", 1, 7, func="tuple")]


def test_it_does_not_crash_on_attribute_functions(flake8dir):
    flake8dir.make_example_py(
        """
        import foo
        bar = foo.baz(x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


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
        foo = {}
        dict(bar=1, **foo)
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C408_pass_6(flake8dir):
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
    assert result.out_lines == [make_message("C408", 1, 1, type="tuple")]


def test_C408_fail_2(flake8dir):
    flake8dir.make_example_py("list()")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C408", 1, 1, type="list")]


def test_C408_fail_3(flake8dir):
    flake8dir.make_example_py("dict()")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C408", 1, 1, type="dict")]


def test_C408_fail_4(flake8dir):
    flake8dir.make_example_py("dict(a=1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C408", 1, 1, type="dict")]


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
        make_message("C409", 1, 7, type="list", func="tuple", suffix="rw")
    ]


def test_C409_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple([1, 2])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C409", 1, 7, type="list", func="tuple", suffix="rw")
    ]


def test_C409_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C409", 1, 7, type="tuple", func="tuple", suffix="rm")
    ]


def test_C409_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple((1, 2))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C409", 1, 7, type="tuple", func="tuple", suffix="rm")
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
        make_message("C410", 1, 7, type="list", func="list", suffix="rm")
    ]


def test_C410_fail_2(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list([1, 2])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C410", 1, 7, type="list", func="list", suffix="rm")
    ]


def test_C410_fail_3(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list(())
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C410", 1, 7, type="tuple", func="list", suffix="rw")
    ]


def test_C410_fail_4(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list((1, 2))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        make_message("C410", 1, 7, type="tuple", func="list", suffix="rw")
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
    assert result.out_lines == [make_message("C411", 1, 1)]


# C412


def test_C412_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        [] == [x + 1 for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C412_pass_2(flake8dir):
    flake8dir.make_example_py(
        """
        10 in (x + 1 for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C412_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        10 in [x + 1 for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C412", 1, 1)]


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

    common = {"outer": "reversed", "inner": "sorted"}
    assert result.out_lines == [
        make_message("C413", 1, 1, outer="list", inner="sorted", suffix=""),
        make_message("C413", 2, 1, suffix="st", value=True, **common),
        make_message("C413", 3, 1, suffix="st", value=True, **common),
        make_message("C413", 4, 1, suffix="st", value=False, **common),
        make_message("C413", 5, 1, suffix="st", value=True, **common),
        make_message("C413", 6, 1, suffix="st", value=False, **common),
        make_message("C413", 7, 1, suffix="tg", value=True, **common),
        make_message("C413", 8, 1, suffix="tg", value=False, **common),
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
        make_message("C414", 2, 1, inner="list", outer="list"),
        make_message("C414", 3, 1, inner="tuple", outer="list"),
        make_message("C414", 4, 1, inner="list", outer="tuple"),
        make_message("C414", 5, 1, inner="tuple", outer="tuple"),
        make_message("C414", 6, 1, inner="set", outer="set"),
        make_message("C414", 7, 1, inner="list", outer="set"),
        make_message("C414", 8, 1, inner="tuple", outer="set"),
        make_message("C414", 9, 1, inner="sorted", outer="set"),
        make_message("C414", 10, 1, inner="sorted", outer="set"),
        make_message("C414", 11, 1, inner="reversed", outer="set"),
        make_message("C414", 12, 1, inner="list", outer="sorted"),
        make_message("C414", 13, 1, inner="tuple", outer="sorted"),
        make_message("C414", 14, 1, inner="sorted", outer="sorted"),
        make_message("C414", 15, 1, inner="sorted", outer="sorted"),
        make_message("C414", 16, 1, inner="sorted", outer="sorted"),
        make_message("C414", 17, 1, inner="sorted", outer="sorted"),
        make_message("C414", 18, 1, inner="reversed", outer="sorted"),
        make_message("C414", 19, 1, inner="reversed", outer="sorted"),
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
        make_message("C415", 1, 1, func="set"),
        make_message("C415", 2, 1, func="sorted"),
        make_message("C415", 3, 1, func="sorted"),
        make_message("C415", 4, 1, func="reversed"),
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


@python_3_6_plus
def test_C416_pass_2_async_list(flake8dir):
    flake8dir.make_example_py(
        """\
        async def foo():
            [x async for x in range(5)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


@python_3_6_plus
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
    assert result.out_lines == [make_message("C416", 1, col_offset, type="list")]


def test_C416_fail_2_set(flake8dir):
    flake8dir.make_example_py("{x for x in range(5)}")
    result = flake8dir.run_flake8()
    assert result.out_lines == [make_message("C416", 1, 1, type="set")]
