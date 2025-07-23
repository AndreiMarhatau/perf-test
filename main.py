"""
PC Performance Test Suite
Tests CPU single-core performance and drive I/O performance
"""

import time
import os
import random
import tempfile
import math

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

        def is_prime(n: int) -> bool:
            """Check if a number is prime"""
            if n < 2:
                return False
            for i in range(2, int(math.sqrt(n)) + 1):
                if n % i == 0:
                    return False
            return True

        def fibonacci(n: int) -> int:
            """Compute Fibonacci number recursively"""
            if n <= 1:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        start_time = time.time()
        prime_count = 0
        operations = 0
        current = 2

        # Run a mix of operations until the duration expires
        while time.time() - start_time < duration:
            if is_prime(current):
                prime_count += 1
            _ = math.sin(current) * math.cos(current) + math.sqrt(current)
            _ = fibonacci(20)
            operations += 1
            current += 1

        cpu_time = time.time() - start_time
        cpu_score = int(operations / cpu_time)

        self.results['cpu'] = {
            'duration': cpu_time,
            'operations': operations,
            'score': cpu_score,
            'primes_found': prime_count
        }

        print(f"   Duration: {cpu_time:.2f}s")
        print(f"   Operations performed: {operations}")
        print(f"   CPU Score: {cpu_score} ops/sec")
    
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
    
    def run_all_tests(self):
        """Run all performance tests"""
        print("🚀 Starting PC Performance Test Suite")
        print("=" * 50)
        
        try:
            # CPU Test
            self.cpu_single_core_test(duration=10)
            print()
            
            # Drive Tests
            self.drive_sequential_test()
            print()
            
            self.drive_random_test()
            print()
            
            # Calculate scores
            cpu_score = self.results['cpu']['score']
            drive_score = self.calculate_drive_score()
            overall_score = int((cpu_score + drive_score) / 2)
            
            # Detailed breakdown
            print("📋 DETAILED BREAKDOWN")
            print("-" * 30)
            cpu = self.results['cpu']
            seq = self.results['sequential']
            rand = self.results['random']
            
            print(f"CPU Tests:")
            print(f"  • Duration: {cpu['duration']:.2f}s")
            print(f"  • Operations: {cpu['operations']}")
            print(f"  • Primes found: {cpu['primes_found']}")
            print()
            
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
            print(f"Drive Performance Score:  {drive_score:8d} composite")
            print(f"Overall Performance Score: {overall_score:8d} combined")
            
        except KeyboardInterrupt:
            print("\n⚠️  Test interrupted by user")
        except Exception as e:
            print(f"\n❌ Error during testing: {e}")
        finally:
            self.cleanup()

def main():
    """Main function to run the performance test"""
    test = PerformanceTest()
    test.run_all_tests()

if __name__ == "__main__":
    main()
