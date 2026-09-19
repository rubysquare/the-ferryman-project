"""
The Ferryman Project — Package execution entrypoint.
Allows running with `python3 -m ferryman`.
"""

import sys
from ferryman.cli import main

if __name__ == "__main__":
    sys.exit(main())
