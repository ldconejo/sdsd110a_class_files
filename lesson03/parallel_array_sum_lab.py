#!/usr/bin/env python3
"""
Parallel Array Sum Lab
Design Patterns and System Design - Class 3

This lab demonstrates:
1. Single vs Multi-threaded array summation
2. Race conditions in shared data access
3. Performance analysis and speedup calculation
4. Thread synchronization with locks
"""

import threading
import time
import random
import matplotlib.pyplot as plt
from typing import List, Tuple
import concurrent.futures
import numpy as np

class ArraySumLab:
    def __init__(self, array_size: int = 1000000):
        """Initialize the lab with a large array for testing."""
        self.array_size = array_size
        self.test_array = [random.randint(1, 100) for _ in range(array_size)]
        self.expected_sum = sum(self.test_array)  # Calculate correct answer
        
        # Variables for demonstrating race conditions
        self.unsafe_sum = 0
        self.safe_sum = 0
        self.lock = threading.Lock()
        
        print(f"🧪 Lab initialized with array of {array_size:,} elements")
        print(f"✓ Expected sum: {self.expected_sum:,}")
        print("-" * 60)

    def single_threaded_sum(self) -> Tuple[int, float]:
        """Calculate sum using single thread and measure time."""
        print("🔄 Running single-threaded sum...")
        
        start_time = time.time()
        result = sum(self.test_array)
        end_time = time.time()
        
        execution_time = end_time - start_time
        print(f"   Result: {result:,}")
        print(f"   Time: {execution_time:.4f} seconds")
        
        return result, execution_time

    def worker_thread_unsafe(self, start_idx: int, end_idx: int):
        """Worker thread that adds to shared variable WITHOUT synchronization."""
        partial_sum = sum(self.test_array[start_idx:end_idx])
        
        # RACE CONDITION: Multiple threads modifying shared variable
        # This will likely produce incorrect results!
        temp = self.unsafe_sum
        time.sleep(0.0001)  # Simulate some processing delay
        self.unsafe_sum = temp + partial_sum

    def worker_thread_safe(self, start_idx: int, end_idx: int):
        """Worker thread that adds to shared variable WITH synchronization."""
        partial_sum = sum(self.test_array[start_idx:end_idx])
        
        # THREAD SAFE: Using lock to protect shared variable
        with self.lock:
            temp = self.unsafe_sum
            time.sleep(0.0001)  # Same delay as unsafe version
            self.safe_sum = temp + partial_sum

    def multi_threaded_sum_unsafe(self, num_threads: int = 4) -> Tuple[int, float]:
        """Calculate sum using multiple threads WITHOUT proper synchronization."""
        print(f"⚠️  Running UNSAFE multi-threaded sum with {num_threads} threads...")
        
        # Reset shared variable
        self.unsafe_sum = 0
        
        # Calculate chunk size for each thread
        chunk_size = len(self.test_array) // num_threads
        threads = []
        
        start_time = time.time()
        
        # Create and start threads
        for i in range(num_threads):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < num_threads - 1 else len(self.test_array)
            
            thread = threading.Thread(target=self.worker_thread_unsafe, 
                                    args=(start_idx, end_idx))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"   Result: {self.unsafe_sum:,}")
        print(f"   Time: {execution_time:.4f} seconds")
        print(f"   ❌ Correct? {self.unsafe_sum == self.expected_sum}")
        
        return self.unsafe_sum, execution_time

    def multi_threaded_sum_safe(self, num_threads: int = 4) -> Tuple[int, float]:
        """Calculate sum using multiple threads WITH proper synchronization."""
        print(f"🔒 Running SAFE multi-threaded sum with {num_threads} threads...")
        
        # Reset shared variable
        self.safe_sum = 0
        
        # Calculate chunk size for each thread
        chunk_size = len(self.test_array) // num_threads
        threads = []
        
        start_time = time.time()
        
        # Create and start threads
        for i in range(num_threads):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size if i < num_threads - 1 else len(self.test_array)
            
            thread = threading.Thread(target=self.worker_thread_safe, 
                                    args=(start_idx, end_idx))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"   Result: {self.safe_sum:,}")
        print(f"   Time: {execution_time:.4f} seconds")
        print(f"   ✅ Correct? {self.safe_sum == self.expected_sum}")
        
        return self.safe_sum, execution_time

    def optimal_multi_threaded_sum(self, num_threads: int = 4) -> Tuple[int, float]:
        """Optimal multi-threaded approach - no shared variables!"""
        print(f"⚡ Running OPTIMAL multi-threaded sum with {num_threads} threads...")
        
        def worker_thread_optimal(start_idx: int, end_idx: int) -> int:
            """Worker that returns its result instead of modifying shared state."""
            return sum(self.test_array[start_idx:end_idx])
        
        # Calculate chunk size
        chunk_size = len(self.test_array) // num_threads
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor for cleaner thread management
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # Submit all tasks
            futures = []
            for i in range(num_threads):
                start_idx = i * chunk_size
                end_idx = start_idx + chunk_size if i < num_threads - 1 else len(self.test_array)
                
                future = executor.submit(worker_thread_optimal, start_idx, end_idx)
                futures.append(future)
            
            # Collect results
            partial_sums = [future.result() for future in futures]
            result = sum(partial_sums)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"   Result: {result:,}")
        print(f"   Time: {execution_time:.4f} seconds")
        print(f"   ✅ Correct? {result == self.expected_sum}")
        
        return result, execution_time

    def run_performance_comparison(self, max_threads: int = 8):
        """Compare performance across different thread counts."""
        print("\n" + "="*60)
        print("📊 PERFORMANCE COMPARISON")
        print("="*60)
        
        # Single-threaded baseline
        _, single_time = self.single_threaded_sum()
        
        thread_counts = [2, 4, 6, 8] if max_threads >= 8 else list(range(2, max_threads + 1))
        times = []
        speedups = []
        
        print(f"\n📈 Testing with different thread counts:")
        print("-" * 40)
        
        for num_threads in thread_counts:
            _, multi_time = self.optimal_multi_threaded_sum(num_threads)
            speedup = single_time / multi_time
            
            times.append(multi_time)
            speedups.append(speedup)
            
            print(f"   {num_threads} threads: {speedup:.2f}x speedup")
        
        return thread_counts, times, speedups, single_time

    def demonstrate_race_conditions(self, iterations: int = 5):
        """Show how race conditions produce inconsistent results."""
        print("\n" + "="*60)
        print("⚠️  RACE CONDITION DEMONSTRATION")
        print("="*60)
        
        print(f"Running unsafe sum {iterations} times to show inconsistent results:")
        print("-" * 50)
        
        results = []
        for i in range(iterations):
            print(f"Run {i+1}:", end=" ")
            result, _ = self.multi_threaded_sum_unsafe(4)
            results.append(result)
        
        print(f"\n📊 Results Analysis:")
        print(f"   Expected: {self.expected_sum:,}")
        print(f"   Actual results: {results}")
        print(f"   Unique values: {len(set(results))}")
        print(f"   All correct? {all(r == self.expected_sum for r in results)}")
        
        if len(set(results)) > 1:
            print("   ❌ RACE CONDITION DETECTED - Inconsistent results!")
        else:
            print("   ⚠️  Race condition may not be visible (try larger array or more iterations)")

def plot_performance_results(thread_counts: List[int], times: List[float], 
                           speedups: List[float], single_time: float):
    """Create visualization of performance results."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Execution time plot
    ax1.plot([1] + thread_counts, [single_time] + times, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Number of Threads')
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('Execution Time vs Thread Count')
    ax1.grid(True, alpha=0.3)
    ax1.set_yscale('log')
    
    # Add annotations
    ax1.annotate(f'Single: {single_time:.4f}s', 
                xy=(1, single_time), xytext=(1.2, single_time*1.5),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    # Speedup plot
    ideal_speedup = thread_counts  # Perfect scaling
    ax2.plot(thread_counts, speedups, 'go-', linewidth=2, markersize=8, label='Actual')
    ax2.plot(thread_counts, ideal_speedup, 'r--', linewidth=2, label='Ideal (Linear)')
    ax2.set_xlabel('Number of Threads')
    ax2.set_ylabel('Speedup Factor')
    ax2.set_title('Speedup vs Thread Count')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def run_complete_lab():
    """Run the complete lab demonstration."""
    print("🚀 PARALLEL ARRAY SUM LAB")
    print("=" * 60)
    print("This lab demonstrates threading concepts, race conditions, and performance.")
    print()
    
    # Create lab instance
    lab = ArraySumLab(array_size=100000000)  # 100 million elements
    
    # Part 1: Basic comparison
    print("\n" + "="*60)
    print("PART 1: BASIC SINGLE vs MULTI-THREADED COMPARISON")
    print("="*60)
    
    single_result, single_time = lab.single_threaded_sum()
    optimal_result, multi_time = lab.optimal_multi_threaded_sum(4)
    
    speedup = single_time / multi_time
    print(f"\n📈 Speedup with 4 threads: {speedup:.2f}x")
    
    # Part 2: Race condition demonstration
    lab.demonstrate_race_conditions()
    
    # Part 3: Safe vs unsafe threading
    print("\n" + "="*60)
    print("PART 3: SAFE vs UNSAFE THREADING")
    print("="*60)
    
    print("Comparing synchronized vs unsynchronized access:")
    lab.multi_threaded_sum_safe(4)
    
    # Part 4: Performance analysis
    thread_counts, times, speedups, single_time = lab.run_performance_comparison()
    
    # Part 5: Visualize results (optional)
    try:
        plot_performance_results(thread_counts, times, speedups, single_time)
    except ImportError:
        print("\n⚠️  Matplotlib not available - skipping visualization")
    
    print("\n" + "="*60)
    print("🎓 LAB COMPLETE - KEY LEARNING POINTS")
    print("="*60)
    print("✅ Single-threaded is simple and always correct")
    print("⚠️  Multi-threading can introduce race conditions")
    print("🔒 Synchronization ensures correctness but adds overhead")
    print("⚡ Best approach: avoid shared state when possible")
    print("📊 Performance gains depend on problem size and thread count")
    print("🖥️  Optimal thread count often matches CPU cores")

if __name__ == "__main__":
    run_complete_lab()
