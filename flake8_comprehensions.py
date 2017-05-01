# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ast

__author__ = 'Adam Johnson'
__email__ = 'me@adamj.eu'
__version__ = '1.3.0'


class ComprehensionChecker(object):
    """
    Flake8 plugin to help you write better list/set/dict comprehensions.
    """
    name = 'flake8-comprehensions'
    version = __version__

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree

    messages = {
        'C400': 'C400 Unnecessary generator - rewrite as a list comprehension.',
        'C401': 'C401 Unnecessary generator - rewrite as a set comprehension.',
        'C402': 'C402 Unnecessary generator - rewrite as a dict comprehension.',
        'C403': 'C403 Unnecessary list comprehension - rewrite as a set comprehension.',
        'C404': 'C404 Unnecessary list comprehension - rewrite as a dict comprehension.',
        'C405': 'C405 Unnecessary {type} literal - rewrite as a set literal.',
        'C406': 'C406 Unnecessary {type} literal - rewrite as a dict literal.',
        'C407': "C407 Unnecessary list comprehension - '{func}' can take a generator.",
    }

    def run(self):
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call) and
                len(node.args) == 1 and
                isinstance(node.func, ast.Name)
            ):
                if (
                    isinstance(node.args[0], ast.GeneratorExp) and
                    node.func.id in ('list', 'set')
                ):
                    msg_key = {
                        'list': 'C400',
                        'set': 'C401',
                    }[node.func.id]
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg_key],
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], ast.GeneratorExp) and
                    isinstance(node.args[0].elt, ast.Tuple) and
                    len(node.args[0].elt.elts) == 2 and
                    node.func.id == 'dict'
                ):
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages['C402'],
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], ast.ListComp) and
                    node.func.id in ('set', 'dict')
                ):
                    msg_key = {
                        'set': 'C403',
                        'dict': 'C404',
                    }[node.func.id]
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg_key],
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], (ast.Tuple, ast.List)) and
                    node.func.id in ('set', 'dict')
                ):
                    msg_key = {
                        'set': 'C405',
                        'dict': 'C406',
                    }[node.func.id]
                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages[msg_key].format(type=type(node.args[0]).__name__.lower()),
                        type(self),
                    )

                elif (
                    isinstance(node.args[0], ast.ListComp) and
                    node.func.id in ('all', 'any', 'frozenset', 'max', 'min', 'sorted', 'sum', 'tuple',)
                ):

                    yield (
                        node.lineno,
                        node.col_offset,
                        self.messages['C407'].format(func=node.func.id),
                        type(self),
                    )
