# PC Performance Test Suite

A comprehensive cross-platform performance testing tool that evaluates your device's CPU single-core and multi-core performance, and drive I/O performance.

## Quick Run

Run the performance test directly without downloading (defaults: single-core, 10s, drive tests skipped; opt in to drive tests with `--with-drive`):
- In bash:
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 -
```
- Powershell:
```pwsh
(iwr -useb https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/windows.py).Content | python -
```

### Common one-liners
- Quick multi-core check (15s, CPU only):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15
```
- Longer CPU stress (10 minutes, multi-core):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 600
```
- Quick single-core sanity test (10s):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode single --cpu-duration 10
```

- Full suite including drive tests (multi-core, 15s):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15 --with-drive
```

**Windows note:** Use `windows.py`; it downloads `main.py` to a temp file, runs it, then deletes the temp file so multiprocessing works from a one-liner.

## CLI Options

- `--cpu-mode {single|multi}`: Choose single-core or multi-core CPU test (default: single)
- `--cpu-duration <seconds>`: CPU test duration in seconds (default: 10)
- `--cpu-workers <N>`: Number of workers in multi-core mode (default: CPU count)
- `--with-drive`: Include drive tests (default is CPU-only)

### Examples

- Default run (single-core, 10s, no drive tests):
```bash
python3 main.py
```

- Multi-core using all cores for 15s:
```bash
python3 main.py --cpu-mode multi --cpu-duration 15
```

- Quick one-liner multi-core without cloning:
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15
```

- Multi-core with 4 workers and full suite (drive tests enabled):
```bash
python3 main.py --cpu-mode multi --cpu-workers 4 --with-drive
```
