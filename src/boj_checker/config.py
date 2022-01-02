from pathlib import Path
from typing import Any, Dict, List

import json


class LanguageConfig:
    """Configuration of compile, run commands.

    Attributes
    ----------
    language_type : str
        Type of the language. One of "scripted", "compiled", "fixed_exec"
    compile_command_template : List[str]
        Template of the compile command, with source and binary path placeholders.
        For example, when using gcc to compile C code,
        `compile_command_template` should be
        ["gcc", "{source_path}", "-o", "{exec_path}"]
    run_command_template : List[str]
        Template of the run command. The format should be the same as
        `compile_command_template`.
    """

    def __init__(
        self,
        language_type: str,
        compile_command_template: List[str],
        run_command_template: List[str],
    ):
        """Create LanguageConfig object.

        Parameters
        ----------
        language_type
            The language type.
        compile_command_template
            Template of the compile command.
        run_command_template
            Template of the run command.
        """
        self.language_type = language_type
        self.compile_command_template = compile_command_template
        self.run_command_template = run_command_template

    @classmethod
    def fromdict(cls, config: Dict[str, Any]) -> "LanguageConfig":
        """Create LanguageConfig object from config dictionary.

        Parameters
        ----------
        config
            The config dictionary to refer to. `config["language_type"]`,
            `config["compile_command"]` and `config["run_command"]` are assigned
            to `language_type`, `compile_command_template` and
            `run_command_template` respectively.

        Returns
        -------
        LanguageConfig
            Created object.
        """
        return cls(
            config["language_type"], config["compile_command"], config["run_command"]
        )

    def compile_command(self, source_path: Path, exec_path: Path) -> List[str]:
        """Create compilation command for subprocess.Popen.

        Parameters
        ----------
        source_path
            The path of the source file to compile.
        exec_path
            The path of the binary. For java-like compiler, this should be a
            path of a directory.

        Returns
        -------
        List[str]
            Compilation command in list format.
        """
        return [
            x.format(source_path=source_path.absolute(), exec_path=exec_path.absolute())
            for x in self.compile_command_template
        ]

    def run_command(self, source_path: Path, exec_path: Path) -> List[str]:
        """Create run command for subprocess.Popen.

        Parameters
        ----------
        source_path
            The path of the source file to compile.
        exec_path
            The path of the binary. For java-like compiler, this should be a
            path of a directory.

        Returns
        -------
        List[str]
            Compilation command in list format.
        """
        return [
            x.format(source_path=source_path.absolute(), exec_path=exec_path.absolute())
            for x in self.run_command_template
        ]


class CheckerConfig:
    """BOJ Checker config file parser.

    Attributes
    ----------
    config_dict : Dict[str, Any]
        A dictionary parsed from config file.
    languageconfig_table : Dict[str, LanguageConfig]
        A dictionary mapping file extension to LanguageConfig object.
    """

    def __init__(self, config_file_content: str):
        """Create CheckerConfig object.

        Parameters
        ----------
        config_file_content
            Content of the config file, in JSON format.
        """
        self.config_dict = json.loads(config_file_content)
        self.languageconfig_table = dict()
        for languageconfig_dict in self.config_dict["language_configs"]:
            self.languageconfig_table[
                languageconfig_dict["extension"]
            ] = LanguageConfig.fromdict(languageconfig_dict["config"])

    @classmethod
    def fromdefault(cls) -> "CheckerConfig":
        """Create CheckerConfig from default configuration. This is equivalent
        of `CheckerConfig('{"language_configs": []}')`.

        Returns
        -------
        CheckerConfig
            Created object.
        """
        return cls('{"language_configs": []}')

    @classmethod
    def fromfilepath(cls, filepath: Path) -> "CheckerConfig":
        """Create CheckerConfig from config file path.

        Parameters
        ----------
        filepath
            Path of the config file.

        Returns
        -------
        CheckerConfig
            Created object.
        """
        with open(filepath) as f:
            content = f.read()
        return cls(content)
