from boj_checker.runner import check_output

import unittest


class TestRunner(unittest.TestCase):
    def test_check_output(self):
        self.assertTrue(check_output("1 1\n", "1 1"))
        self.assertTrue(check_output("1 1\r\n", "1 1"))
        self.assertFalse(check_output("1 1\n", " 1 1"))
        self.assertFalse(check_output("1 1\n", "1 2"))
        self.assertTrue(check_output("1\r\n2 3\r\n", "1\n2 3"))
        self.assertTrue(check_output("1\r\n2 3\r\n", "1\n2 3\n"))
        self.assertFalse(check_output("1\r\n2 3\r\n", "1\n 2 3\n"))
        self.assertFalse(check_output("1\r\n2 3\r\n", " 1\n2 3\n"))
