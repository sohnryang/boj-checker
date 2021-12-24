from pathlib import Path
from subprocess import Popen, PIPE
from typing import Tuple
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


def run_source_file(filepath: Path, input_str: str) -> Tuple[str, int]:
    """Run a source file from given path, getting input from `input_str`.

    Parameters
    ----------
    filepath
        The path of the source file to run.
    input_str
        The input to provide.

    Returns
    -------
    Tuple[str, int]
        The output of the program, and the exit code.

    Raises
    ------
    NotImplementedError
        If this function cannot handle the filetype of the source.
    """
    dirname = generate_dirname(filepath)
    temp_dir_path = temporary_dir_root() / dirname
    os.mkdir(temp_dir_path)
    file_extension = filepath.suffix[1:]
    try:
        language_type, compile_command, run_command = extension_lookup[file_extension]
    except KeyError:
        raise NotImplementedError(f"Not implemented for extension: {file_extension}")

    if language_type == "scripted":
        process = Popen(run_command(filepath), stdout=PIPE, stdin=PIPE)
    elif language_type == "fixed_exec":
        assert compile_command != None
        compile_process = Popen(compile_command(filepath, temp_dir_path))
        exit_code = compile_process.wait()
        if exit_code != 0:
            raise ValueError(f"Compilation of source {filepath} failed")
        process = Popen(run_command(Path()), stdout=PIPE, stdin=PIPE, cwd=temp_dir_path)
    else:
        assert compile_command != None
        compile_process = Popen(compile_command(filepath, temp_dir_path / "a.out"))
        exit_code = compile_process.wait()
        if exit_code != 0:
            raise ValueError(f"Compilation of source {filepath} failed")
        process = Popen(run_command(temp_dir_path / "a.out"), stdout=PIPE, stdin=PIPE)

    output, _ = process.communicate(input=input_str.encode("utf-8"))
    exit_code = process.wait()

    for path, _, filenames in os.walk(temp_dir_path):
        for filename in filenames:
            full_path = os.path.join(path, filename)
            if os.path.exists(full_path):
                os.remove(full_path)
    os.rmdir(temp_dir_path)
    return (output.decode("utf-8"), exit_code)