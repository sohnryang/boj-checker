from pathlib import Path
from typing import Callable, List, NamedTuple, Union
from .config import LanguageConfig


class LanguageInfo(NamedTuple):
    language_type: str
    compile_command: Union[Callable[[Path, Path], List[str]], None]
    run_command: Callable[[Path], List[str]]


extension_lookup = {
    "py": LanguageConfig("scripted", [], ["python3", "{source_path}"]),
    "c": LanguageConfig(
        "compiled", ["gcc", "{source_path}", "-o", "{exec_path}"], ["{exec_path}"]
    ),
    "cc": LanguageConfig(
        "compiled", ["g++", "{source_path}", "-o", "{exec_path}"], ["{exec_path}"]
    ),
    "java": LanguageConfig(
        "fixed_exec",
        [
            "javac",
            "{source_path}",
            "-d",
            "{exec_path}",
        ],
        ["java", "Main"],
    ),
    "rs": LanguageConfig(
        "compiled", ["rustc", "{source_path}", "-o", "{exec_path}"], ["{exec_path}"]
    ),
}
