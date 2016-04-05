# -*- encoding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import ast

__author__ = 'Adam Johnson'
__email__ = 'me@adamj.eu'
__version__ = '1.0.0'


class ComprehensionChecker(object):
    """
    Flake8 plugin to help you write better list/set/dict comprehensions.
    """
    name = 'flake8-comprehensions'
    version = __version__

    def __init__(self, tree, *args, **kwargs):
        self.tree = tree

    message_C100 = 'C100 Unnecessary generator - rewrite as a list comprehension.'
    message_C101 = 'C101 Unnecessary generator - rewrite as a set comprehension.'
    message_C102 = 'C102 Unnecessary generator - rewrite as a dict comprehension.'

    def run(self):
        for node in ast.walk(self.tree):
            if (
                isinstance(node, ast.Call) and
                len(node.args) == 1 and
                isinstance(node.args[0], ast.GeneratorExp)
            ):
                if node.func.id == 'list':
                    yield (node.lineno, node.col_offset, self.message_C100, type(self))
                elif node.func.id == 'set':
                    yield (node.lineno, node.col_offset, self.message_C101, type(self))
                elif node.func.id == 'dict':
                    yield (node.lineno, node.col_offset, self.message_C102, type(self))
