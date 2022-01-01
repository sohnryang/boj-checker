"""BOJ checker -- check solutions against IO samples"""
__version__ = "1.0.0b1"
from .cli import main
import sys


def entry():
    exit(main(sys.argv[1:]))
