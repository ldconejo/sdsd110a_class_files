# memory_explorer_complete.py
import psutil
import os
import time
import matplotlib.pyplot as plt
from collections import deque
import gc

class MemoryExplorer:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.memory_usage = []
        self.timestamps = []
        self.labels = []
        self.start_time = time.time()
        
    def record_memory(self, label=""):
        """Record current memory usage with optional label"""
        # Force garbage collection for accurate measurements
        gc.collect()
        
        current_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        current_time = time.time() - self.start_time
        self.memory_usage.append(current_memory)
        self.timestamps.append(current_time)
        self.labels.append(label)
        print(f"[{current_time:.2f}s] {label}: {current_memory:.2f} MB")
        
    def get_object_size(self, obj):
        """Get approximate size of object in MB"""
        import sys
        return sys.getsizeof(obj) / 1024 / 1024
        
    def plot_memory_usage(self):
        """Plot memory usage over time"""
        plt.figure(figsize=(12, 8))
        
        # Main plot
        plt.subplot(2, 1, 1)
        plt.plot(self.timestamps, self.memory_usage, 'b-o', linewidth=2)
        
        # Add labels for significant points
        for i, label in enumerate(self.labels):
            if label and 'Baseline' not in label:
                plt.annotate(label, 
                            (self.timestamps[i], self.memory_usage[i]),
                            textcoords="offset points",
                            xytext=(0,10),
                            ha='center',
                            fontsize=8,
                            bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
        
        plt.xlabel('Time (seconds)')
        plt.ylabel('Memory Usage (MB)')
        plt.title('Process Memory Usage Over Time')
        plt.grid(True, alpha=0.3)
        
        # Delta plot
        plt.subplot(2, 1, 2)
        if len(self.memory_usage) > 1:
            baseline = self.memory_usage[0]
            deltas = [m - baseline for m in self.memory_usage]
            plt.plot(self.timestamps, deltas, 'r-o', linewidth=2)
            plt.xlabel('Time (seconds)')
            plt.ylabel('Memory Delta from Baseline (MB)')
            plt.title('Memory Growth from Baseline')
            plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def experiment_1_list_growth():
    """Experiment 1: How lists grow in memory"""
    print("\n=== Experiment 1: List Growth Patterns ===")
    explorer = MemoryExplorer()
    
    # Baseline
    explorer.record_memory("Baseline")
    time.sleep(0.5)
    
    # Create list and observe growth
    data = []
    sizes = [100000, 500000, 1000000, 2000000]
    
    for size in sizes:
        for i in range(len(data), size):
            data.append(i)
        explorer.record_memory(f"List size: {len(data):,}")
        time.sleep(0.5)
    
    # Clear and observe
    data.clear()
    explorer.record_memory("After clear()")
    
    del data
    explorer.record_memory("After del")
    
    explorer.plot_memory_usage()

def experiment_2_data_structure_comparison():
    """Experiment 2: Compare different data structures"""
    print("\n=== Experiment 2: Data Structure Comparison ===")
    explorer = MemoryExplorer()
    
    # Baseline
    explorer.record_memory("Baseline")
    time.sleep(0.5)
    
    n = 1000000
    
    # Test 1: List of integers
    print("\nCreating list of integers...")
    list_data = list(range(n))
    explorer.record_memory(f"List[int] ({n:,} items)")
    list_size = explorer.get_object_size(list_data)
    print(f"List object size: {list_size:.2f} MB")
    time.sleep(0.5)
    
    # Test 2: Dictionary
    print("\nCreating dictionary...")
    dict_data = {i: f"value_{i}" for i in range(n)}
    explorer.record_memory(f"Dict ({n:,} items)")
    dict_size = explorer.get_object_size(dict_data)
    print(f"Dict object size: {dict_size:.2f} MB")
    time.sleep(0.5)
    
    # Test 3: Set
    print("\nCreating set...")
    set_data = set(range(n))
    explorer.record_memory(f"Set ({n:,} items)")
    set_size = explorer.get_object_size(set_data)
    print(f"Set object size: {set_size:.2f} MB")
    time.sleep(0.5)
    
    # Test 4: Deque
    print("\nCreating deque...")
    deque_data = deque(range(n))
    explorer.record_memory(f"Deque ({n:,} items)")
    deque_size = explorer.get_object_size(deque_data)
    print(f"Deque object size: {deque_size:.2f} MB")
    time.sleep(0.5)
    
    # Clean up
    del list_data, dict_data, set_data, deque_data
    explorer.record_memory("After cleanup")
    
    explorer.plot_memory_usage()

def experiment_3_string_concatenation():
    """Experiment 3: String operations memory impact"""
    print("\n=== Experiment 3: String Operations ===")
    explorer = MemoryExplorer()
    
    # Baseline
    explorer.record_memory("Baseline")
    
    # Bad way: String concatenation
    print("\nString concatenation (inefficient)...")
    bad_string = ""
    for i in range(50000):
        bad_string += f"{i},"
        if i % 10000 == 0:
            explorer.record_memory(f"Concat {i:,} items")
    
    del bad_string
    explorer.record_memory("After del bad_string")
    time.sleep(0.5)
    
    # Good way: List join
    print("\nList join (efficient)...")
    good_list = []
    for i in range(50000):
        good_list.append(f"{i}")
        if i % 10000 == 0:
            explorer.record_memory(f"List {i:,} items")
    
    good_string = ",".join(good_list)
    explorer.record_memory("After join")
    
    del good_list, good_string
    explorer.record_memory("Final cleanup")
    
    explorer.plot_memory_usage()

def interactive_exploration():
    """Interactive mode for students to experiment"""
    print("\n=== Interactive Memory Explorer ===")
    explorer = MemoryExplorer()
    
    print("Commands:")
    print("  baseline - Record baseline memory")
    print("  list N - Create list with N integers")
    print("  dict N - Create dictionary with N items")
    print("  string N - Create string by concatenating N items")
    print("  clear - Clear all variables")
    print("  plot - Show memory plot")
    print("  quit - Exit")
    
    variables = {}
    
    while True:
        cmd = input("\n> ").strip().split()
        if not cmd:
            continue
            
        if cmd[0] == "quit":
            break
        elif cmd[0] == "baseline":
            explorer.record_memory("Baseline")
        elif cmd[0] == "plot":
            explorer.plot_memory_usage()
        elif cmd[0] == "clear":
            variables.clear()
            gc.collect()
            explorer.record_memory("After clear")
        elif cmd[0] == "list" and len(cmd) > 1:
            n = int(cmd[1])
            variables['list_data'] = list(range(n))
            explorer.record_memory(f"List({n})")
        elif cmd[0] == "dict" and len(cmd) > 1:
            n = int(cmd[1])
            variables['dict_data'] = {i: f"val_{i}" for i in range(n)}
            explorer.record_memory(f"Dict({n})")
        elif cmd[0] == "string" and len(cmd) > 1:
            n = int(cmd[1])
            variables['string_data'] = "".join(str(i) for i in range(n))
            explorer.record_memory(f"String({n})")
        else:
            print("Unknown command")

def main():
    """Main lab execution"""
    print("Memory Usage Explorer Lab")
    print("=" * 50)
    
    while True:
        print("\nSelect an experiment:")
        print("1. List Growth Patterns")
        print("2. Data Structure Comparison")
        print("3. String Operations")
        print("4. Interactive Exploration")
        print("5. Exit")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            experiment_1_list_growth()
        elif choice == "2":
            experiment_2_data_structure_comparison()
        elif choice == "3":
            experiment_3_string_concatenation()
        elif choice == "4":
            interactive_exploration()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
