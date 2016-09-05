#!/usr/bin/env python3


import unittest

from .context import wcf


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.c = wcf.WCF()

    def test_if_initialized(self):
        self.assertEqual(bool(self.c), False)

    def test_string_output(self):
        self.assertEqual(str(self.c), 'WCF API connection: NOT ACTIVE')

    def test_load_user(self):
        self.c._load_user('/home/mikemoran/bin/wcf/credentials.json')
        self.assertIn('Username', self.c.credentials)
        self.assertIn('Password', self.c.credentials)
