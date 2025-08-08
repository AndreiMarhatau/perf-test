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
(iwr -useb https://raw.githubusercontent.com/AndreiMarhatau/perf-test/main/main.py).Content | python - --cpu-mode multi --cpu-duration 15 --skip-drive
```

### iPhone
Use one of the apps that let you run python code, or even bash commands. A-shell works well - just run above bash command there.

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
