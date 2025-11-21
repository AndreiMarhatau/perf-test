"""
Windows entry point: fetches the main suite script to a temp file and runs it,
so multiprocessing works even when invoked via a piped one-liner. The temp file
is deleted after execution.
"""

import os
import subprocess
import sys
import tempfile
from urllib.request import urlopen

MAIN_URL = "https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py"


def run():
    fd, temp_path = tempfile.mkstemp(prefix="perf_test_main_", suffix=".py")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(urlopen(MAIN_URL).read())

        result = subprocess.run([sys.executable, temp_path] + sys.argv[1:])
        sys.exit(result.returncode)
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


if __name__ == "__main__":
    run()
