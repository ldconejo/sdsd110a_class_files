import time
import math
from collections import Counter

# Global variables for storing results
stats_cache = {}

def calculate_mean(numbers):
    """Calculate arithmetic mean"""
    return sum(numbers) / len(numbers)

def calculate_median(numbers):
    """Calculate median value"""
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2 if n % 2 == 0 else sorted_nums[mid]

def find_mode(numbers):
    """Find most frequent number"""
    counts = Counter(numbers)
    max_count = max(counts.values())
    modes = [num for num, count in counts.items() if count == max_count]
    return "No mode (all scores unique)" if len(modes) == len(numbers) else (modes[0] if len(modes) == 1 else modes)

def calculate_range(numbers):
    """Calculate range (max - min)"""
    return max(numbers) - min(numbers)

def calculate_std_dev(numbers):
    """Calculate standard deviation"""
    mean = calculate_mean(numbers)
    variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
    return math.sqrt(variance)

def generate_stats_report(numbers):
    """Generate complete statistics report"""
    global stats_cache
    
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    mode = find_mode(numbers)
    data_range = calculate_range(numbers)
    std_dev = calculate_std_dev(numbers)

    stats_cache = {
        "mean": mean,
        "median": median,
        "mode": mode,
        "range": data_range,
        "std_dev": std_dev,
    }

    report = (
        f"=== STATISTICS REPORT ===\n"
        f"Data: {numbers}\n"
        f"Count: {len(numbers)} scores\n"
        f"Mean: {mean:.2f}\n"
        f"Median: {median:.2f}\n"
        f"Mode: {mode}\n"
        f"Range: {data_range} ({min(numbers)} to {max(numbers)})\n"
        f"Std Dev: {std_dev:.2f}\n"
    )

    print(report)
    return stats_cache

def process_statistics_procedural(numbers):
    """Main procedural processing function"""
    start_time = time.time()
    
    generate_stats_report(numbers)
    
    end_time = time.time()
    print(f"Procedural processing time: {end_time - start_time:.4f} seconds")

# Test data
test_scores = [85, 92, 78, 90, 88, 76, 95, 82, 87, 91]
test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 82, 87, 82, 91]
test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 87, 82, 91]

if __name__ == "__main__":
    process_statistics_procedural(test_scores)
