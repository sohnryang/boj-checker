from pathlib import Path
from boj_checker.config import LanguageConfig

import unittest


class TestConfig(unittest.TestCase):
    def test_language_config(self):
        langcfg = LanguageConfig(
            "compiled",
            ["clang++", "{source_path}", "-o", "{exec_path}"],
            ["{exec_path}"],
        )
        self.assertIsNotNone(langcfg)
        self.assertListEqual(
            langcfg.compile_command(Path("./t.cc"), Path("./a.out")),
            [
                "clang++",
                str(Path("./t.cc").absolute()),
                "-o",
                str(Path("./a.out").absolute()),
            ],
        )
        self.assertListEqual(
            langcfg.run_command(Path("./t.cc"), Path("./a.out")),
            [str(Path("./a.out").absolute())],
        )

        langcfg2 = LanguageConfig.fromdict(
            {
                "language_type": "compiled",
                "compile_command": ["clang++", "{source_path}", "-o", "{exec_path}"],
                "run_command": ["{exec_path}"],
            }
        )
        self.assertIsNotNone(langcfg2)
        self.assertListEqual(
            langcfg2.compile_command(Path("./t.cc"), Path("./a.out")),
            [
                "clang++",
                str(Path("./t.cc").absolute()),
                "-o",
                str(Path("./a.out").absolute()),
            ],
        )
        self.assertListEqual(
            langcfg2.run_command(Path("./t.cc"), Path("./a.out")),
            [str(Path("./a.out").absolute())],
        )
