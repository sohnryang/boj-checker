# boj-checker

백준 코드 자동 테스트하기

BOJ에 제출하기 전, 예제 입력을 자동으로 테스트하는 도구입니다. [`act`](https://github.com/nektos/act), [`trevor`](https://github.com/vadimdemedes/trevor)와 같은 도구에서 아이디어를 얻었습니다.

## Showcase

[![asciicast](https://asciinema.org/a/KHaQAJegMjlWENiSuJK2bXrGG.svg)](https://asciinema.org/a/KHaQAJegMjlWENiSuJK2bXrGG)

## 설치 방법

`boj-checker`는 PyPI에서 다운로드할 수 있습니다. Python 3.7 이상의 파이썬 인터프리터가 권장됩니다.

```shell
$ pip install -U boj-checker
```

> Python으로 작성되긴 했지만, `boj-checker`는 아직 Windows를 지원하지 않으니 주의 바랍니다.

## 사용법

다음과 같이 명령어를 입력하면 자동으로 테스트됩니다.

```shell
$ boj-checker $prob_no $source_path
```

여기서 `$prob_no`에는 문제 번호를, `$source_path`에는 테스트할 코드의 경로를 입력하면 됩니다.

이외의 옵션에 대해서는 `boj-checker --help`의 출력을 참조 바랍니다.

## 언어 지원

`boj-checker`는 기본적으로 다음과 같은 언어들을 지원합니다.

- C/C++ (`gcc`, `g++` 사용)

- Python (CPython 사용)

- Java

- Rust (`rustc` 사용)

## 설정 파일

기본적으로 지원되는 것 이외의 언어를 사용하거나, 다른 컴파일러 또는 런타임을 이용하고 싶은 경우 설정 파일을 사용할 수 있습니다. `boj-checker`는 XDG 디렉토리 표준 명세을 따르기 때문에, `$XDG_CONFIG_HOME`(보통 `~/.config/boj-checker/config.json`)에서 설정 파일을 로드합니다. 다음은 파이썬 코드 실행에 `pypy3`를, C++ 코드 컴파일에 `clang++`을 사용하는 설정 파일의 예입니다.

```json
{
  "language_configs": [
    {
      "extension": "py",
      "config": {
        "language_type": "scripted",
        "compile_command": [],
        "run_command": ["pypy3", "{source_path}"]
      }
    },
    {
      "extension": "cc",
      "config": {
        "language_type": "compiled",
        "compile_command": ["clang++", "{source_path}", "-o", "{exec_path}"],
        "run_command": ["{exec_path}"]
      }
    }
  ]
}
```

`language_type`에는 `scripted`, `compiled`, `fixed_exec` 세 가지 값이 가능합니다. 각각으 의미는 다음과 같습니다.

- `scripted`: Python, Ruby와 같이 별도의 컴파일 과정이 필요 없는 스크립트 언어입니다.

- `compiled`: C/C++과 같이 컴파일 과정이 필요한 언어입니다.

- `fixed_exec`: Java와 같이 컴파일 과정이 필요하지만, 컴파일 결과물의 파일명을 지정할 수 없는 언어입니다.

 `compile_command`, `run_command`에는 컴파일, 실행 명령어가 단어 단위로 끊은 리스트 형태로 저장됩니다. 소스 코드 경로가 들어갈 곳에는 `{source_path}`, 실행 파일의 경로(`language_type`이 `fixed_exec`인 경우에는 실행 파일이 저장된 디렉토리의 경로)가 들어갈 곳에는 `{exec_path}`를 사용하면 됩니다.

테스트 등의 목적으로 설정 파일을 `$XDG_CONFIG_HOME` 이외의 경로에서 로드할 경우에는 `--config` 옵션을, 설정 파일을 아예 로드하지 않는 경우에는 `--no-config` 옵션을 사용할 수 있습니다.
