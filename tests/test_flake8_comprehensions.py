import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version


def test_version(flake8dir):
    result = flake8dir.run_flake8(["--version"])
    version_string = (
        "flake8-comprehensions: " + version("flake8-comprehensions")
    )
    assert version_string in result.out_lines[0]


# C400


def test_C400_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = [x for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C400_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = list(x for x in range(10))
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
        foo = {x for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C401_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set(x for x in range(10))
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
        foo = {x for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C403_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = set([x for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C403 Unnecessary list comprehension - rewrite as a "
        + "set comprehension."
    ]


# C404


def test_C404_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = {x: x for x in range(10)}
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C404_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = dict([(x, x) for x in range(10)])
    """
    )
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


# C407


def test_C407_sum_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = sum(x for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_sum_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = sum([x for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C407 Unnecessary list comprehension - 'sum' can take "
        + "a generator."
    ]


def test_C407_max_pass_1(flake8dir):
    flake8dir.make_example_py("max(x for x in range(10))")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_pass_2(flake8dir):
    flake8dir.make_example_py("max((x for x in range(10)), key=lambda x: x * 2)")
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_pass_3(flake8dir):
    flake8dir.make_example_py(
        "max((x for x in range(10)), default=1, key=lambda x: x * 2)"
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_max_fail_1(flake8dir):
    flake8dir.make_example_py("max([x for x in range(10)])")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C407 Unnecessary list comprehension - 'max' can take "
        + "a generator."
    ]


def test_C407_max_fail_2(flake8dir):
    flake8dir.make_example_py("max([x for x in range(10)], default=1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C407 Unnecessary list comprehension - 'max' can take "
        + "a generator."
    ]


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
    flake8dir.make_example_py("enumerate([x for x in range(10)])")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C407 Unnecessary list comprehension - 'enumerate' "
        + "can take a generator."
    ]


def test_C407_enumerate_fail_2(flake8dir):
    flake8dir.make_example_py("enumerate([x for x in range(10)], 1)")
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C407 Unnecessary list comprehension - 'enumerate' "
        + "can take a generator."
    ]


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
        foo = tuple(x for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C407_tuple_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        foo = tuple([x for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:7: C407 Unnecessary list comprehension - 'tuple' can "
        + "take a generator."
    ]


def test_it_does_not_crash_on_attribute_functions(flake8dir):
    flake8dir.make_example_py(
        """
        import foo
        bar = foo.baz(x for x in range(10))
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
        [x for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C411_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        list([x for x in range(10)])
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C411 Unnecessary list call - remove the outer call "
        + "to list()."
    ]


# C412


def test_C412_pass_1(flake8dir):
    flake8dir.make_example_py(
        """
        [] == [x for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C412_pass_2(flake8dir):
    flake8dir.make_example_py(
        """
        10 in (x for x in range(10))
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == []


def test_C412_fail_1(flake8dir):
    flake8dir.make_example_py(
        """
        10 in [x for x in range(10)]
    """
    )
    result = flake8dir.run_flake8()
    assert result.out_lines == [
        "./example.py:1:1: C412 Unnecessary list comprehension - 'in' can "
        + "take a generator."
    ]
