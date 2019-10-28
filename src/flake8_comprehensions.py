import ast
import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version


class ComprehensionChecker:
    """
    Flake8 plugin to help you write better list/set/dict comprehensions.
    """

    name = "flake8-comprehensions"
    version = version("flake8-comprehensions")

    def __init__(self, tree, *args, **kwargs):
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
        "C407": "C407 Unnecessary list comprehension - '{func}' can take a generator.",
        "C408": "C408 Unnecessary {type} call - rewrite as a literal.",
        "C409": "C409 Unnecessary {type} passed to tuple() - ",
        "C410": "C410 Unnecessary {type} passed to list() - ",
        "C411": "C411 Unnecessary list call - remove the outer call to list().",
        "C412": "C412 Unnecessary list comprehension - 'in' can take a generator.",
    }

    def run(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                num_positional_args = len(node.args)

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
                    and isinstance(node.args[0], ast.GeneratorExp)
                    and isinstance(node.args[0].elt, ast.Tuple)
                    and len(node.args[0].elt.elts) == 2
                    and node.func.id == "dict"
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C402"],
                        type(self),
                    )

                elif (
                    num_positional_args == 1
                    and isinstance(node.args[0], ast.ListComp)
                    and node.func.id in ("list", "set", "dict")
                ):
                    msg_key = {"list": "C411", "set": "C403", "dict": "C404"}[
                        node.func.id
                    ]
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg_key],
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
                    and isinstance(node.args[0], (ast.Tuple, ast.List))
                    and node.func.id in ("tuple", "list", "set", "dict")
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
                    num_positional_args == 1
                    and isinstance(node.args[0], ast.ListComp)
                    and node.func.id
                    in (
                        "all",
                        "any",
                        "frozenset",
                        "tuple",
                        # These take 1 positional argument + some keyword arguments
                        "max",
                        "min",
                        "sorted",
                    )
                ):

                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C407"].format(func=node.func.id),
                        type(self),
                    )

                elif (
                    num_positional_args in (1, 2)
                    and isinstance(node.args[0], ast.ListComp)
                    and node.func.id
                    in (
                        # These can take a second positional argument
                        "enumerate",
                        "sum",
                    )
                ):

                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C407"].format(func=node.func.id),
                        type(self),
                    )

                elif (
                    num_positional_args == 0
                    and not has_star_args(node)
                    and not has_keyword_args(node)
                    and node.func.id in ("tuple", "list", "dict")
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C408"].format(type=node.func.id),
                        type(self),
                    )
            elif isinstance(node, ast.Compare):
                if (
                    len(node.ops) == 1
                    and isinstance(node.ops[0], ast.In)
                    and len(node.comparators) == 1
                    and isinstance(node.comparators[0], ast.ListComp)
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages["C412"],
                        type(self),
                    )


def has_star_args(call_node):
    return any(isinstance(a, ast.Starred) for a in call_node.args)


def has_keyword_args(call_node):
    return any(k.arg is None for k in call_node.keywords)
