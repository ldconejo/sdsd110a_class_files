#!/usr/bin/env python3
"""
Simple Thread-Safe Counter Assignment
Design Patterns and System Design - Class 3
Time: 1 hour
"""

import threading
import time
import random

# ============================================================================
# PART 1: Unsafe Counter (Demonstrates Race Conditions)
# ============================================================================

class UnsafeCounter:
    """
    Counter with NO thread safety - will have race conditions.
    This shows the same problem you saw in the Array Sum lab.
    """
    
    def __init__(self):
        self.value = 0
        self.operations_count = 0
    
    def increment(self):
        """Increment counter by 1."""
        # RACE CONDITION: These steps can be interrupted by other threads
        temp = self.value
        time.sleep(0.0001)  # Simulate some processing time
        self.value = temp + 1
        self.operations_count += 1
    
    def decrement(self):
        """Decrement counter by 1."""
        temp = self.value
        time.sleep(0.0001)  # Simulate some processing time  
        self.value = temp - 1
        self.operations_count += 1
    
    def get_value(self):
        """Get current counter value."""
        return self.value
    
    def reset(self):
        """Reset counter to zero."""
        self.value = 0
        self.operations_count = 0

# ============================================================================
# PART 2: Thread-Safe Counter (YOUR IMPLEMENTATION)
# ============================================================================

class ThreadSafeCounter:
    """
    YOUR TASK: Make this counter thread-safe using locks.
    """
    
    def __init__(self):
        self.value = 0
        self.operations_count = 0
        self._lock = threading.Lock() 
    
    def increment(self):
        temp = self.value
        time.sleep(0.0001)  # Same delay as unsafe version
        self.value = temp + 1
        self.operations_count += 1
    
    def decrement(self):
        temp = self.value
        time.sleep(0.0001)
        self.value = temp - 1
        self.operations_count += 1
    
    def get_value(self):
        return self.value
    
    def reset(self):
        self.value = 0
        self.operations_count = 0

# ============================================================================
# PART 3: Testing Framework
# ============================================================================

def test_counter(counter, num_threads=4, operations_per_thread=1000):
    """
    Test a counter with multiple threads and compute the true expected value
    based on actual increments/decrements performed.
    
    Args:
        counter: Counter instance to test
        num_threads: Number of threads to create
        operations_per_thread: Operations each thread performs
    
    Returns:
        (final_value, expected_value, execution_time, is_correct)
    """
    counter.reset()
    
    results = []  # will hold (increments, decrements) tuples from each thread
    results_lock = threading.Lock()  # to protect access to results list
    
    def worker():
        """Each thread runs this function."""
        local_increments = 0
        local_decrements = 0
        for _ in range(operations_per_thread):
            if random.random() < 0.7:  # 70% increments, 30% decrements
                counter.increment()
                local_increments += 1
            else:
                counter.decrement()
                local_decrements += 1
        # Safely record local counts
        with results_lock:
            results.append((local_increments, local_decrements))
    
    # Start timing
    start_time = time.time()
    
    # Create and start all threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
    
    # Stop timing
    end_time = time.time()
    execution_time = end_time - start_time
    
    # Compute actual expected value based on what really happened
    total_increments = sum(r[0] for r in results)
    total_decrements = sum(r[1] for r in results)
    expected_value = total_increments - total_decrements
    
    final_value = counter.get_value()
    is_correct = (final_value == expected_value)
    
    return final_value, expected_value, execution_time, is_correct

def run_race_condition_demo():
    """Demonstrate race conditions with unsafe counter."""
    print("🏁 RACE CONDITION DEMONSTRATION")
    print("=" * 50)
    print("Running unsafe counter 5 times with same parameters...")
    print("(If working correctly, you should see different results each time)")
    print()
    
    results = []
    for i in range(5):
        counter = UnsafeCounter()
        final_value, expected_value, exec_time, is_correct = test_counter(counter, 4, 500)
        results.append(final_value)
        
        status = "✅ CORRECT" if is_correct else "❌ WRONG"
        print(f"Run {i+1}: {final_value} (expected: {expected_value}) - {status}")
    
    print(f"\nAll results: {results}")
    print(f"Unique results: {len(set(results))}")
    
    if len(set(results)) > 1:
        print("🔍 SUCCESS: Race condition detected! Results vary between runs.")
    else:
        print("⚠️  No race condition visible. Try increasing thread count or operations.")

def run_performance_comparison():
    """Compare performance of unsafe vs safe counters."""
    print("\n⚡ PERFORMANCE COMPARISON")
    print("=" * 50)
    
    # Test parameters
    num_threads = 4
    operations_per_thread = 2000
    
    # Test unsafe counter
    print("Testing Unsafe Counter...")
    unsafe_counter = UnsafeCounter()
    unsafe_result, unsafe_expected, unsafe_time, unsafe_correct = test_counter(
        unsafe_counter, num_threads, operations_per_thread
    )
    
    # Test thread-safe counter
    print("Testing Thread-Safe Counter...")
    safe_counter = ThreadSafeCounter()
    safe_result, safe_expected, safe_time, safe_correct = test_counter(
        safe_counter, num_threads, operations_per_thread
    )
    
    # Display results
    print("\nRESULTS:")
    print("-" * 30)
    print(f"Unsafe Counter:")
    print(f"  Result: {unsafe_result} (expected: {unsafe_expected})")
    print(f"  Correct: {'✅ Yes' if unsafe_correct else '❌ No'}")
    print(f"  Time: {unsafe_time:.3f} seconds")
    
    print(f"\nThread-Safe Counter:")
    print(f"  Result: {safe_result} (expected: {safe_expected})")
    print(f"  Correct: {'✅ Yes' if safe_correct else '❌ No'}")
    print(f"  Time: {safe_time:.3f} seconds")
    
    # Performance comparison
    if unsafe_time > 0 and safe_time > 0:
        speed_ratio = unsafe_time / safe_time
        if speed_ratio > 1:
            print(f"\n📊 Thread-safe counter is {speed_ratio:.2f}x SLOWER than unsafe")
        else:
            print(f"\n📊 Thread-safe counter is {1/speed_ratio:.2f}x FASTER than unsafe")
        
        print("This is the trade-off between CORRECTNESS and PERFORMANCE")

# ============================================================================
# PART 4: Main Assignment Runner
# ============================================================================

def main():
    """Run the complete assignment."""
    print("🎓 THREAD-SAFE COUNTER ASSIGNMENT")
    print("Design Patterns and System Design - Class 3")
    print("Estimated time: 1 hour")
    print("=" * 60)
    
    # Part 1: Show the problem
    run_race_condition_demo()
    
    # Part 2: Compare solutions  
    run_performance_comparison()
    
if __name__ == "__main__":
    main()
