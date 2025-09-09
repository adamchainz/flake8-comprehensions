from __future__ import annotations

import ast
from collections.abc import Generator
from importlib.metadata import version
from typing import Any


class ComprehensionChecker:
    """
    Flake8 plugin to help you write better list/set/dict comprehensions.
    """

    name = "flake8-comprehensions"
    version = version("flake8-comprehensions")

    __slots__ = ("tree",)

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    messages = {
        "C400": "C400 Unnecessary generator - rewrite as a list comprehension.",
        "C401": "C401 Unnecessary generator - rewrite as a set comprehension.",
        "C402": "C402 Unnecessary generator - rewrite as a dict comprehension.",
        "C403": "C403 Unnecessary list comprehension - rewrite as a set comprehension.",
        "C404": (
            "C404 Unnecessary list comprehension - rewrite as a dict comprehension."
        ),
        "C405": "C405 Unnecessary {type} literal - ",
        "C406": "C406 Unnecessary {type} literal - ",
        "C408": "C408 Unnecessary {type} call - rewrite as a literal.",
        "C409": "C409 Unnecessary {type} passed to tuple() - ",
        "C410": "C410 Unnecessary {type} passed to list() - ",
        "C411": "C411 Unnecessary list call - remove the outer call to list().",
        "C413": "C413 Unnecessary {outer} call around {inner}(){remediation}.",
        "C414": "C414 Unnecessary {inner} call within {outer}().",
        "C415": "C415 Unnecessary subscript reversal of iterable within {func}().",
        "C416": "C416 Unnecessary {type} comprehension - rewrite using {type}().",
        "C417": "C417 Unnecessary use of map - use a {comp} instead.",
        "C418": (
            "C418 Unnecessary {type} passed to dict() - "
            + "remove the outer call to dict()."
        ),
        "C419": (
            "C419 Unnecessary list comprehension passed to {func}() prevents "
            + "short-circuiting - rewrite as a generator."
        ),
        "C420": (
            "C420 Unnecessary {type} comprehension - rewrite using dict.fromkeys()."
        ),
    }

    def run(self) -> Generator[tuple[int, int, str, type[Any]]]:
        # Stores previously seen map() nodes, to avoid raising C417 on it twice.
        visited_map_calls: set[ast.Call] = set()

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                num_positional_args = len(node.args)
                num_keyword_args = len(node.keywords)

                if (
                    num_positional_args == 1
                    and isinstance(node.args[0], ast.GeneratorExp)
                    and node.func.id in ("list", "set")
                ):
                    msg_key = {"list": "C400", "set": "C401"}[node.func.id]
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg_key],
                        type(self),
                    )

                elif (
                    num_positional_args == 1
                    and node.func.id == "dict"
                    and len(node.keywords) == 0
                    and isinstance(node.args[0], (ast.GeneratorExp, ast.ListComp))
                    and isinstance(node.args[0].elt, ast.Tuple)
                    and len(node.args[0].elt.elts) == 2
                ):
                    if isinstance(node.args[0], ast.GeneratorExp):
                        msg = "C402"
                    else:
                        msg = "C404"
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg],
                        type(self),
                    )

                elif (
                    num_positional_args == 1
                    and isinstance(node.args[0], ast.ListComp)
                    and node.func.id in ("list", "set", "any", "all")
                ):
                    msg_key = {
                        "list": "C411",
                        "set": "C403",
                        "any": "C419",
                        "all": "C419",
                    }[node.func.id]
                    msg = self.messages[msg_key].format(func=node.func.id)
                    yield (
                        node.lineno,
                        node.col_offset,
                        msg,
                        type(self),
                    )

                elif num_positional_args == 1 and (
                    isinstance(node.args[0], ast.Tuple)
                    and node.func.id == "tuple"
                    or isinstance(node.args[0], ast.List)
                    and node.func.id == "list"
                ):
                    suffix = "remove the outer call to {func}()."
                    msg_key = {"tuple": "C409", "list": "C410"}[node.func.id]
                    msg = self.messages[msg_key] + suffix
                    yield (
                        node.lineno,
                        node.col_offset,
                        msg.format(
                            type=type(node.args[0]).__name__.lower(), func=node.func.id
                        ),
                        type(self),
                    )

                elif (
                    num_positional_args == 1
                    and num_keyword_args == 0
                    and isinstance(node.args[0], (ast.Dict, ast.DictComp))
                    and node.func.id == "dict"
                ):
                    if isinstance(node.args[0], ast.Dict):
                        type_ = "dict"
                    else:
                        type_ = "dict comprehension"
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C418"].format(type=type_),
                        type(self),
                    )

                elif (
                    num_positional_args == 1
                    and isinstance(node.args[0], (ast.Tuple, ast.List))
                    and (
                        node.func.id in ("tuple", "list", "set")
                        or (
                            node.func.id == "dict"
                            and all(
                                isinstance(i, ast.Tuple) and len(i.elts) == 2
                                for i in node.args[0].elts
                            )
                        )
                    )
                ):
                    suffix = "rewrite as a {func} literal."
                    msg_key = {
                        "tuple": "C409",
                        "list": "C410",
                        "set": "C405",
                        "dict": "C406",
                    }[node.func.id]
                    msg = self.messages[msg_key] + suffix
                    yield (
                        node.lineno,
                        node.col_offset,
                        msg.format(
                            type=type(node.args[0]).__name__.lower(), func=node.func.id
                        ),
                        type(self),
                    )

                elif (
                    num_positional_args == 0
                    and not has_star_args(node)
                    and not has_double_star_args(node)
                    and node.func.id == "dict"
                ) or (
                    num_positional_args == 0
                    and num_keyword_args == 0
                    and node.func.id in ("tuple", "list")
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C408"].format(type=node.func.id),
                        type(self),
                    )

                elif (
                    node.func.id in {"list", "reversed"}
                    and num_positional_args > 0
                    and isinstance(node.args[0], ast.Call)
                    and isinstance(node.args[0].func, ast.Name)
                    and node.args[0].func.id == "sorted"
                ):
                    remediation = ""
                    if node.func.id == "reversed":
                        reverse_flag_value: bool | None = False
                        for keyword in node.args[0].keywords:
                            if keyword.arg != "reverse":
                                continue
                            if isinstance(keyword.value, ast.Constant):
                                reverse_flag_value = bool(keyword.value.value)
                            else:
                                # Complex value
                                reverse_flag_value = None

                        if reverse_flag_value is None:
                            remediation = " - toggle reverse argument to sorted()"
                        else:
                            remediation = f" - use sorted(..., reverse={not reverse_flag_value!r})"

                    msg = self.messages["C413"].format(
                        inner=node.args[0].func.id,
                        outer=node.func.id,
                        remediation=remediation,
                    )
                    yield (
                        node.lineno,
                        node.col_offset,
                        msg,
                        type(self),
                    )

                elif (
                    num_positional_args > 0
                    and isinstance(node.args[0], ast.Call)
                    and isinstance(node.args[0].func, ast.Name)
                    and (
                        (
                            node.func.id in {"set", "sorted"}
                            and node.args[0].func.id
                            in {"list", "reversed", "sorted", "tuple"}
                        )
                        or (
                            node.func.id in {"list", "tuple"}
                            and node.args[0].func.id in {"list", "tuple"}
                        )
                        or (node.func.id == "set" and node.args[0].func.id == "set")
                    )
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C414"].format(
                            inner=node.args[0].func.id, outer=node.func.id
                        ),
                        type(self),
                    )

                elif (
                    node.func.id in {"reversed", "set", "sorted"}
                    and num_positional_args > 0
                    and isinstance(node.args[0], ast.Subscript)
                    and isinstance(node.args[0].slice, ast.Slice)
                    and node.args[0].slice.lower is None
                    and node.args[0].slice.upper is None
                    and isinstance(node.args[0].slice.step, ast.UnaryOp)
                    and isinstance(node.args[0].slice.step.op, ast.USub)
                    and isinstance(node.args[0].slice.step.operand, ast.Constant)
                    and node.args[0].slice.step.operand.value == 1
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C415"].format(func=node.func.id),
                        type(self),
                    )

                elif (
                    node.func.id == "map"
                    and node not in visited_map_calls
                    and len(node.args) == 2
                    and isinstance(node.args[0], ast.Lambda)
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C417"].format(comp="generator expression"),
                        type(self),
                    )

                elif (
                    node.func.id in ("list", "set", "dict")
                    and len(node.args) == 1
                    and isinstance(node.args[0], ast.Call)
                    and isinstance(node.args[0].func, ast.Name)
                    and node.args[0].func.id == "map"
                    and len(node.args[0].args) == 2
                    and isinstance(node.args[0].args[0], ast.Lambda)
                ):
                    # To avoid raising C417 on the map() call inside the list/set/dict.
                    map_call = node.args[0]
                    visited_map_calls.add(map_call)

                    rewriteable = True
                    if node.func.id == "dict":
                        # For the generator expression to be rewriteable as a
                        # dict comprehension, its lambda must return a 2-tuple.
                        lambda_node = node.args[0].args[0]
                        if (
                            not isinstance(lambda_node.body, (ast.List, ast.Tuple))
                            or len(lambda_node.body.elts) != 2
                        ):
                            rewriteable = False

                    if rewriteable:
                        comprehension_type = f"{node.func.id} comprehension"
                        yield (
                            node.lineno,
                            node.col_offset,
                            self.messages["C417"].format(comp=comprehension_type),
                            type(self),
                        )

            elif isinstance(node, (ast.DictComp, ast.ListComp, ast.SetComp)):
                if (
                    len(node.generators) == 1
                    and not node.generators[0].ifs
                    and not node.generators[0].is_async
                ):
                    if (
                        isinstance(node, (ast.ListComp, ast.SetComp))
                        and isinstance(node.elt, ast.Name)
                        and isinstance(node.generators[0].target, ast.Name)
                        and node.elt.id == node.generators[0].target.id
                    ) or (
                        isinstance(node, ast.DictComp)
                        and isinstance(node.key, ast.Name)
                        and isinstance(node.value, ast.Name)
                        and isinstance(node.generators[0].target, ast.Tuple)
                        and len(node.generators[0].target.elts) == 2
                        and isinstance(node.generators[0].target.elts[0], ast.Name)
                        and node.generators[0].target.elts[0].id == node.key.id
                        and isinstance(node.generators[0].target.elts[1], ast.Name)
                        and node.generators[0].target.elts[1].id == node.value.id
                    ):
                        yield (
                            node.lineno,
                            node.col_offset,
                            self.messages["C416"].format(
                                type=comp_type[node.__class__]
                            ),
                            type(self),
                        )

                    elif (
                        isinstance(node, ast.DictComp)
                        and isinstance(node.key, ast.Name)
                        and isinstance(node.value, ast.Constant)
                        and isinstance(node.generators[0].target, ast.Name)
                        and node.key.id == node.generators[0].target.id
                    ):
                        yield (
                            node.lineno,
                            node.col_offset,
                            self.messages["C420"].format(
                                type=comp_type[node.__class__]
                            ),
                            type(self),
                        )


def has_star_args(call_node: ast.Call) -> bool:
    return any(isinstance(a, ast.Starred) for a in call_node.args)


def has_double_star_args(call_node: ast.Call) -> bool:
    return any(k.arg is None for k in call_node.keywords)


comp_type = {
    ast.DictComp: "dict",
    ast.ListComp: "list",
    ast.SetComp: "set",
}
