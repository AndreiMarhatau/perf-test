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
- Quick drive smoke test with a smaller sequential file:
```bash
curl -fsSL https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py | python3 - --with-drive --drive-size-mb 128
```

**Windows note:** Use `windows.py`; it downloads `main.py` to a temp file, runs it, then deletes the temp file so multiprocessing works from a one-liner.

## CLI Options

- `--cpu-mode {single|multi}`: Choose single-core or multi-core CPU test (default: single)
- `--cpu-duration <seconds>`: CPU test duration in seconds (default: 10)
- `--cpu-workers <N>`: Number of workers in multi-core mode (default: CPU count)
- `--with-drive`: Include drive tests (default is CPU-only)
- `--drive-size-mb <MB>`: Sequential drive test file size (default: 1024 MB)

## Interpreting CPU Results

The CPU score is reported as `SHA-256 MiB/sec`. It means how many 1 MiB chunks the CPU can hash per second using Python's standard-library SHA-256 implementation. Higher is better; this is CPU hashing throughput, not drive speed.

## Interpreting Drive Results

The drive test is a simple cross-platform filesystem smoke test, not a raw SSD benchmark. It uses regular Python file I/O on every platform.

Sequential write uses a 1 GiB test file by default, writes deterministic non-compressible data, and includes `fsync` before reporting write throughput. This makes the write value the most useful drive number in the suite.

Sequential read and random I/O can be affected by the OS filesystem cache. They are useful for local smoke checks, but they should not be treated as raw device throughput or used as a strict cross-platform hardware comparison.

Use `--drive-size-mb` for a faster smoke run. Smaller files run faster but are more likely to be affected by cache and filesystem behavior.

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
