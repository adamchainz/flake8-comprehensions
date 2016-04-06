# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ast

__author__ = 'Adam Johnson'
__email__ = 'me@adamj.eu'
__version__ = '1.1.0'


class ComprehensionChecker(object):
    """
    Flake8 plugin to help you write better list/set/dict comprehensions.
    """
    name = 'flake8-comprehensions'
    version = __version__

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree

    message_C400 = 'C400 Unnecessary generator - rewrite as a {type} comprehension.'
    message_C401 = 'C401 Unnecessary list comprehension - rewrite as a {type} comprehension.'
    message_C402 = 'C402 Unnecessary list literal - rewrite as a {type} literal.'

    def run(self):
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call) and
                len(node.args) == 1
            ):
                if (
                    isinstance(node.args[0], ast.GeneratorExp) and
                    node.func.id in ('list', 'set', 'dict')
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.message_C400.format(type=node.func.id),
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], ast.ListComp) and
                    node.func.id in ('set', 'dict')
                ):

                    yield (
                        node.lineno,
                        node.col_offset,
                        self.message_C401.format(type=node.func.id),
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], ast.List) and
                    node.func.id in ('set', 'dict')
                ):

                    yield (
                        node.lineno,
                        node.col_offset,
                        self.message_C402.format(type=node.func.id),
                        type(self),
                    )
