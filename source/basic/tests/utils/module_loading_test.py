# -*- coding: utf-8 -*-
"""
    >File    : module_loading_test.py
    >Author  : YJD
    >Mail    : jindu.yin@digitalbrain.cn
    >Time    : 2022/11/15 15:33
"""

import unittest
import types
from utils.module_loading import import_module, import_string, importlib_find


class TestModuleLoading(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_import_string(self):
        dot_path = 'utils.module_loading.import_string'
        result = import_string(dot_path)
        self.assertTrue(isinstance(result, types.FunctionType))
        # self.assertTrue(callable(result))

    def test_module_has_submodule(self):
        pass

    def test_module_dir(self):
        pass


if __name__ == '__main__':
    unittest.main()
