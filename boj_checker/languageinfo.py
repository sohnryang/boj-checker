from pathlib import Path
from typing import Callable, List, NamedTuple, Union


class LanguageInfo(NamedTuple):
    language_type: str
    compile_command: Union[Callable[[Path, Path], List[str]], None]
    run_command: Callable[[Path], List[str]]


extension_lookup = {
    "py": LanguageInfo(
        "scripted", None, lambda source_path: ["python3", str(source_path.absolute())]
    ),
    "c": LanguageInfo(
        "compiled",
        lambda source_path, exec_path: [
            "gcc",
            str(source_path.absolute()),
            "-o",
            str(exec_path.absolute()),
        ],
        lambda exec_path: [str(exec_path.absolute())],
    ),
    "cc": LanguageInfo(
        "compiled",
        lambda source_path, exec_path: [
            "g++",
            str(source_path.absolute()),
            "-o",
            str(exec_path.absolute()),
        ],
        lambda exec_path: [str(exec_path.absolute())],
    ),
    "java": LanguageInfo(
        "fixed_exec",
        lambda source_path, exec_dir: [
            "javac",
            str(source_path.absolute()),
            "-d",
            str(exec_dir.absolute()),
        ],
        lambda _: ["java", "Main"],
    ),
    "rs": LanguageInfo(
        "compiled",
        lambda source_path, exec_path: [
            "rustc",
            str(source_path.absolute()),
            "-o",
            str(exec_path.absolute()),
        ],
        lambda exec_path: [str(exec_path.absolute())],
    ),
}
