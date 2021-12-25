"""BOJ checker -- check solutions against IO samples"""

import sys
from .cli import main

if __name__ == "__main__":
    exit(main(sys.argv[1:]))
