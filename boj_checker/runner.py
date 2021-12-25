from pathlib import Path
from subprocess import Popen, PIPE
from typing import Dict, Tuple

from boj_checker.config import LanguageConfig
from .languageinfo import extension_lookup

import hashlib
import os


def generate_dirname(filepath: Path) -> str:
    """Create a dirname using given file path.

    Parameters
    ----------
    filepath
        The path of the source file to base on.

    Returns
    -------
    str
        Generated dirname in $filename-$sha256hash format
    """
    hasher = hashlib.sha256()
    BUFSIZE = 65536
    with open(filepath, "rb") as f:
        while True:
            data = f.read(BUFSIZE)
            if not data:
                break
            hasher.update(data)
    return f"{filepath.name}-{hasher.hexdigest()}"


def temporary_dir_root() -> Path:
    """Fetch the location of temporary directory according to OS standard.

    Returns
    -------
    pathlib.Path
        Path object of temporary directory
    """
    return Path("/tmp")  # TODO: support other OSes other than Linux


def run_source_file(
    filepath: Path, input_str: str, user_language_config: Dict[str, LanguageConfig]
) -> Tuple[str, int]:
    """Run a source file from given path, getting input from `input_str`.

    Parameters
    ----------
    filepath
        The path of the source file to run.
    input_str
        The input to provide.
    user_language_config
        Dictionary mapping extension to LanguageConfig object, for custom
        settings.

    Returns
    -------
    Tuple[str, int]
        The output of the program, and the exit code.

    Raises
    ------
    NotImplementedError
        If this function cannot handle the filetype of the source.
    ValueError
        If the compilation of the source code is failed.
    """
    dirname = generate_dirname(filepath)
    temp_dir_path = temporary_dir_root() / dirname
    try:
        os.mkdir(temp_dir_path)
    except FileExistsError:
        pass
    file_extension = filepath.suffix[1:]
    try:
        if file_extension in user_language_config:
            language_info = user_language_config[file_extension]
        else:
            language_info = extension_lookup[file_extension]
    except KeyError:
        raise NotImplementedError(f"Not implemented for extension: {file_extension}")

    if language_info.language_type == "scripted":
        process = Popen(
            language_info.run_command(filepath, Path()), stdout=PIPE, stdin=PIPE
        )
    elif language_info.language_type == "fixed_exec":
        compile_process = Popen(language_info.compile_command(filepath, temp_dir_path))
        exit_code = compile_process.wait()
        if exit_code != 0:
            raise ValueError(f"Compilation of source {filepath} failed")
        process = Popen(
            language_info.run_command(Path(), Path()),
            stdout=PIPE,
            stdin=PIPE,
            cwd=temp_dir_path,
        )
    else:
        compile_process = Popen(
            language_info.compile_command(filepath, temp_dir_path / "a.out")
        )
        exit_code = compile_process.wait()
        if exit_code != 0:
            raise ValueError(f"Compilation of source {filepath} failed")
        process = Popen(
            language_info.run_command(Path(), temp_dir_path / "a.out"),
            stdout=PIPE,
            stdin=PIPE,
        )

    output, _ = process.communicate(input=input_str.encode("utf-8"))
    exit_code = process.wait()

    return (output.decode("utf-8"), exit_code)


def clean_temporary_files(filepath: Path):
    """Clean up a temporary directory created when running source in `filepath`

    Parameters
    ----------
    filepath
        Path of the source.
    """
    dirname = generate_dirname(filepath)
    temp_dir_path = temporary_dir_root() / dirname
    for path, _, filenames in os.walk(temp_dir_path):
        for filename in filenames:
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
    try:
        os.rmdir(temp_dir_path)
    except FileNotFoundError:
        pass


def check_output(solution: str, output: str) -> bool:
    """Check if program's output is correct.

    Parameters
    ----------
    solution
        Sample output taken from BOJ.
    output
        Output from program run.

    Returns
    -------
    bool
        True if correct, False if wrong.
    """
    solution_lines = [x.rstrip() for x in solution.rstrip().split("\n")]
    output_lines = [x.rstrip() for x in output.rstrip().split("\n")]
    return all([x == y for x, y in zip(solution_lines, output_lines)])
