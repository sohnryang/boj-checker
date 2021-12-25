from boj_checker.boj_parser import fetch_sample_io

import unittest


class TestBOJParser(unittest.TestCase):
    def test_fetch_sample_io(self):
        self.assertEqual(fetch_sample_io(10831), [])
        self.assertIsNotNone(fetch_sample_io(1000))
