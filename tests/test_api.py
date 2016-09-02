#!/usr/bin/env python3


import unittest

from .context import wcf


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.c = wcf.WCF()

    def test_string_output(self):
        self.assertEqual(str(self.c), 'WCF API connection: NOT ACTIVE')
