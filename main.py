"""
PC Performance Test Suite
Tests CPU single-core and multi-core performance, and drive I/O performance
"""

import time
import os
import random
import tempfile
import math
import argparse
import multiprocessing as mp
from typing import Optional


def _is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def _fibonacci(n: int) -> int:
    """Compute Fibonacci number recursively (intentionally CPU heavy)"""
    if n <= 1:
        return n
    return _fibonacci(n - 1) + _fibonacci(n - 2)


def _cpu_burn_worker(duration: float, num_slices: int = 10) -> dict:
    """Worker that burns CPU for approximately `duration` seconds.

    Returns dict with operations, primes_found, and measured duration.
    """
    start_time = time.time()
    prime_count = 0
    operations = 0
    current = 2
    # Track operations per time slice for simple timeseries output
    ops_slices = [0] * max(1, int(num_slices))
    slice_len = duration / len(ops_slices) if duration > 0 else 1.0
    next_cutoff = slice_len  # seconds since start
    slice_idx = 0

    while time.time() - start_time < duration:
        if _is_prime(current):
            prime_count += 1
        _ = math.sin(current) * math.cos(current) + math.sqrt(current)
        _ = _fibonacci(20)
        operations += 1
        current += 1
        # Increment current slice counter, advance slice when passing cutoff
        if slice_idx < len(ops_slices):
            ops_slices[slice_idx] += 1
            elapsed = time.time() - start_time
            while elapsed >= next_cutoff and slice_idx < len(ops_slices) - 1:
                slice_idx += 1
                next_cutoff += slice_len

    elapsed = time.time() - start_time
    return {"operations": operations, "primes_found": prime_count, "duration": elapsed, "ops_slices": ops_slices}

class PerformanceTest:
    def __init__(self):
        self.results = {}
        self.temp_dir = tempfile.mkdtemp(prefix="perf_test_")
        
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def cpu_single_core_test(self, duration=10):
        """Test CPU single-core performance for a fixed duration"""
        print("🔥 Testing CPU Single-Core Performance...")
        slices = 10
        slice_dur = duration / slices if duration > 0 else 1.0
        ops_slices = []
        total_ops = 0
        prime_total = 0
        bar_width = 40
        max_rate_seen = 0.0
        print("   CPU ops/sec over time:")
        start_total = time.time()
        for i in range(slices):
            res = _cpu_burn_worker(slice_dur, num_slices=1)
            ops = res["operations"]
            prime = res["primes_found"]
            elapsed = res["duration"] or slice_dur
            total_ops += ops
            prime_total += prime
            ops_slices.append(ops)
            rate = ops / elapsed if elapsed > 0 else 0
            if rate > max_rate_seen:
                max_rate_seen = rate
            bar_len = int((rate / max_rate_seen) * bar_width) if max_rate_seen > 0 else 0
            lo = int(i * (100 / slices))
            hi = int((i + 1) * (100 / slices))
            print(f"    {i+1:02d} [{lo:02d}-{hi:02d}%] {('█' * bar_len).ljust(bar_width)} {int(rate)}", flush=True)

        cpu_time = time.time() - start_total
        cpu_score = int(total_ops / cpu_time) if cpu_time > 0 else 0

        self.results['cpu'] = {
            'mode': 'single',
            'duration': cpu_time,
            'operations': total_ops,
            'score': cpu_score,
            'primes_found': prime_total,
            'workers': 1,
            'ops_slices': ops_slices,
            'slice_count': len(ops_slices),
            'planned_duration': duration
        }

        print(f"    max≈{int(max_rate_seen)} ops/s")
        print(f"   Duration: {cpu_time:.2f}s")
        print(f"   Operations performed: {total_ops}")
        print(f"   CPU Score: {cpu_score} ops/sec")

    def cpu_multi_core_test(self, duration=10, workers: Optional[int] = None):
        """Test CPU multi-core performance by running N workers in parallel."""
        if workers is None or workers <= 0:
            workers = os.cpu_count() or 1
        print(f"🔥 Testing CPU Multi-Core Performance with {workers} workers...")

        # Prefer fork when available so the script can run from stdin/one-liners
        # without requiring an importable module path (spawn fails for `<stdin>`).
        start_method = "fork" if "fork" in mp.get_all_start_methods() else "spawn"
        ctx = mp.get_context(start_method)

        slices = 10
        slice_dur = duration / slices if duration > 0 else 1.0
        total_ops = 0
        total_primes = 0
        total_wall_time = 0.0
        agg_slices = []
        bar_width = 40
        max_rate_seen = 0.0
        print("   CPU ops/sec over time:")
        with ctx.Pool(processes=workers) as pool:
            for i in range(slices):
                results = pool.starmap(_cpu_burn_worker, [(slice_dur, 1)] * workers)
                slice_ops = sum(r["operations"] for r in results)
                slice_primes = sum(r["primes_found"] for r in results)
                slice_time = max(r["duration"] for r in results) if results else slice_dur
                total_ops += slice_ops
                total_primes += slice_primes
                total_wall_time += slice_time
                agg_slices.append(slice_ops)

                rate = slice_ops / slice_time if slice_time > 0 else 0
                if rate > max_rate_seen:
                    max_rate_seen = rate
                bar_len = int((rate / max_rate_seen) * bar_width) if max_rate_seen > 0 else 0
                lo = int(i * (100 / slices))
                hi = int((i + 1) * (100 / slices))
                print(f"    {i+1:02d} [{lo:02d}-{hi:02d}%] {('█' * bar_len).ljust(bar_width)} {int(rate)}", flush=True)

        cpu_score = int(total_ops / total_wall_time) if total_wall_time > 0 else 0

        self.results['cpu'] = {
            'mode': 'multi',
            'duration': total_wall_time,
            'operations': total_ops,
            'score': cpu_score,
            'primes_found': total_primes,
            'workers': workers,
            'ops_slices': agg_slices,
            'slice_count': len(agg_slices),
            'planned_duration': duration
        }

        print(f"    max≈{int(max_rate_seen)} ops/s")
        print(f"   Duration: {total_wall_time:.2f}s")
        print(f"   Total operations: {total_ops}")
        print(f"   Aggregate CPU Score: {cpu_score} ops/sec")
    
    def drive_sequential_test(self, file_size_mb=100):
        """Test sequential read/write performance"""
        print("💾 Testing Drive Sequential Performance...")
        
        test_file = os.path.join(self.temp_dir, "sequential_test.dat")
        data_chunk = b'A' * (1024 * 1024)  # 1MB chunk
        
        # Sequential Write Test
        start_time = time.time()
        with open(test_file, 'wb') as f:
            for _ in range(file_size_mb):
                f.write(data_chunk)
        write_time = time.time() - start_time
        write_speed = file_size_mb / write_time  # MB/s
        
        # Sequential Read Test
        start_time = time.time()
        with open(test_file, 'rb') as f:
            while f.read(1024 * 1024):
                pass
        read_time = time.time() - start_time
        read_speed = file_size_mb / read_time  # MB/s
        
        # Clean up
        os.remove(test_file)
        
        self.results['sequential'] = {
            'write_time': write_time,
            'read_time': read_time,
            'write_speed_mb_s': write_speed,
            'read_speed_mb_s': read_speed,
            'file_size_mb': file_size_mb
        }
        
        print(f"   Sequential Write: {write_speed:.1f} MB/s")
        print(f"   Sequential Read: {read_speed:.1f} MB/s")
    
    def drive_random_test(self, num_operations=1000):
        """Test random read/write performance"""
        print("🎲 Testing Drive Random Performance...")
        
        # Create a test file with random data
        test_file = os.path.join(self.temp_dir, "random_test.dat")
        file_size = 50 * 1024 * 1024  # 50MB
        
        # Create file with random data
        with open(test_file, 'wb') as f:
            for _ in range(50):
                f.write(os.urandom(1024 * 1024))
        
        # Random Read Test
        start_time = time.time()
        with open(test_file, 'rb') as f:
            for _ in range(num_operations):
                # Random seek and read 4KB
                pos = random.randint(0, file_size - 4096)
                f.seek(pos)
                f.read(4096)
        random_read_time = time.time() - start_time
        
        # Random Write Test
        start_time = time.time()
        with open(test_file, 'r+b') as f:
            for _ in range(num_operations):
                # Random seek and write 4KB
                pos = random.randint(0, file_size - 4096)
                f.seek(pos)
                f.write(os.urandom(4096))
        random_write_time = time.time() - start_time
        
        # Calculate IOPS (Input/Output Operations Per Second)
        read_iops = num_operations / random_read_time
        write_iops = num_operations / random_write_time
        
        # Clean up
        os.remove(test_file)
        
        self.results['random'] = {
            'read_time': random_read_time,
            'write_time': random_write_time,
            'read_iops': read_iops,
            'write_iops': write_iops,
            'operations': num_operations
        }
        
        print(f"   Random Read: {read_iops:.0f} IOPS")
        print(f"   Random Write: {write_iops:.0f} IOPS")
    
    def calculate_drive_score(self):
        """Calculate overall drive performance score as composite metric"""
        seq = self.results['sequential']
        rand = self.results['random']
        
        # Create a composite score that combines all metrics
        # Sequential throughput (MB/s) + Random IOPS weighted
        # This gives a single number that represents overall drive performance
        drive_score = int(
            (seq['write_speed_mb_s'] + seq['read_speed_mb_s']) / 2 +
            (rand['read_iops'] + rand['write_iops']) / 100
        )
        
        return drive_score
    
    def run_all_tests(self, cpu_mode: str = 'single', cpu_duration: int = 10, cpu_workers: Optional[int] = None, skip_drive: bool = False):
        """Run all performance tests"""
        print("🚀 Starting PC Performance Test Suite")
        print("=" * 50)
        
        try:
            # CPU Test
            if cpu_mode == 'multi':
                self.cpu_multi_core_test(duration=cpu_duration, workers=cpu_workers)
            else:
                self.cpu_single_core_test(duration=cpu_duration)
            print()
            
            # Drive Tests (optional)
            if not skip_drive:
                self.drive_sequential_test()
                print()
                
                self.drive_random_test()
                print()
            
            # Calculate scores
            cpu_score = self.results['cpu']['score']
            if not skip_drive:
                drive_score = self.calculate_drive_score()
                overall_score = int((cpu_score + drive_score) / 2)
            else:
                drive_score = None
                overall_score = cpu_score
            
            # Detailed breakdown
            print("📋 DETAILED BREAKDOWN")
            print("-" * 30)
            cpu = self.results['cpu']
            if not skip_drive:
                seq = self.results['sequential']
                rand = self.results['random']
            
            print(f"CPU Tests:")
            print(f"  • Mode: {cpu['mode']} ({cpu['workers']} worker(s))")
            print(f"  • Duration: {cpu['duration']:.2f}s")
            print(f"  • Operations: {cpu['operations']}")
            print(f"  • Primes found: {cpu['primes_found']}")
            
            if not skip_drive:
                print(f"Drive Tests:")
                print(f"  • Sequential Write: {seq['write_speed_mb_s']:.1f} MB/s")
                print(f"  • Sequential Read: {seq['read_speed_mb_s']:.1f} MB/s")
                print(f"  • Random Read: {rand['read_iops']:.0f} IOPS")
                print(f"  • Random Write: {rand['write_iops']:.0f} IOPS")
                print()
            
            # Display final results
            print("📊 PERFORMANCE RESULTS")
            print("=" * 50)
            print(f"CPU Performance Score:    {cpu_score:8d} ops/sec")
            if not skip_drive:
                print(f"Drive Performance Score:  {drive_score:8d} composite")
                print(f"Overall Performance Score: {overall_score:8d} combined")
            else:
                print(f"Overall Performance Score: {overall_score:8d} (CPU only)")
            
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
        finally:
            self.cleanup()

def main():
    """Main function to run the performance test"""
    parser = argparse.ArgumentParser(description="PC Performance Test Suite")
    parser.add_argument("--cpu-mode", choices=["single", "multi"], default="single", help="CPU test mode")
    parser.add_argument("--cpu-duration", type=int, default=10, help="CPU test duration in seconds")
    parser.add_argument("--cpu-workers", type=int, default=None, help="Number of workers for multi-core test (default: CPU count)")
    parser.add_argument("--skip-drive", action="store_true", help="Skip drive tests and run CPU only")
    args = parser.parse_args()

    test = PerformanceTest()
    test.run_all_tests(cpu_mode=args.cpu_mode, cpu_duration=args.cpu_duration, cpu_workers=args.cpu_workers, skip_drive=args.skip_drive)

if __name__ == "__main__":
    main()
