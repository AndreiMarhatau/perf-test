# PC Performance Test Suite

A comprehensive cross-platform performance testing tool that evaluates your device's CPU single-core and multi-core performance, and drive I/O performance.

## Quick Run

Run the performance test directly without downloading (you can pass flags after `-`):
- In bash:
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15 --skip-drive
```
- Powershell:
```pwsh
(iwr -useb https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/windows.py).Content | python - --cpu-mode multi --cpu-duration 15 --skip-drive
```
- iOS (a-Shell):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/ios.py | python3 - --cpu-mode multi --cpu-duration 15 --skip-drive
```

### Common one-liners
- Quick multi-core check (15s):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15
```
- Longer CPU stress (10 minutes, multi-core, skip drive):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 600 --skip-drive
```
- Quick single-core sanity test (10s):
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode single --cpu-duration 10
```

**Windows note:** Use `windows.py`; it downloads `main.py` to a temp file, runs it, then deletes the temp file so multiprocessing works from a one-liner.
**iPhone note:** Use `ios.py`; it downloads `main.py` to a temp file, runs it, then deletes the temp file so multiprocessing works from a one-liner in a-Shell.

## CLI Options

- `--cpu-mode {single|multi}`: Choose single-core or multi-core CPU test (default: single)
- `--cpu-duration <seconds>`: CPU test duration in seconds (default: 10)
- `--cpu-workers <N>`: Number of workers in multi-core mode (default: CPU count)
- `--skip-drive`: Skip drive tests and run CPU only

### Examples

- Single-core CPU only for 10s:
```bash
python3 main.py --cpu-mode single --skip-drive
```

- Multi-core using all cores for 15s:
```bash
python3 main.py --cpu-mode multi --cpu-duration 15 --skip-drive
```

- Quick one-liner multi-core without cloning:
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --cpu-mode multi --cpu-duration 15 --skip-drive
```

- Multi-core with 4 workers and full suite:
```bash
python3 main.py --cpu-mode multi --cpu-workers 4
```
