import time
import math
from functools import reduce
from collections import Counter

def calculate_mean(numbers):
    """Pure function to calculate mean"""
    # Using reduce to sum the numbers
    # Initial value of 0 for the accumulator
    # Dividing by length of numbers to get mean
    return reduce(lambda acc, x: acc + x, numbers, 0) / len(numbers)

def calculate_median(numbers):
    """Pure function to calculate median"""
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    # Double forward slash for floor division
    # which divides the first operand by the second and rounds down to the nearest integer
    mid = n // 2
    return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2 if n % 2 == 0 else sorted_nums[mid]

def find_mode(numbers):
    """Pure function to find mode"""
    counts = Counter(numbers)
    max_count = max(counts.values())
    # Return all modes if multiple share the max frequency
    modes = [num for num, count in counts.items() if count == max_count]
    return "No mode (all scores unique)" if max_count == 1 else modes[0] if len(modes) == 1 else modes

def calculate_range(numbers):
    """Pure function to calculate range"""
    return max(numbers) - min(numbers)

def calculate_std_dev(numbers):
    """Pure function to calculate standard deviation"""
    mean = calculate_mean(numbers)
    variance = reduce(lambda acc, x: acc + (x - mean) ** 2, numbers, 0) / len(numbers)
    return math.sqrt(variance)

def calculate_all_stats(numbers):
    """Pure function to calculate all statistics"""
    return {
        "mean": calculate_mean(numbers),
        "median": calculate_median(numbers),
        "mode": find_mode(numbers),
        "range": calculate_range(numbers),
        "std_dev": calculate_std_dev(numbers),
    }

def format_report(numbers, stats):
    """Pure function to format report"""
    return (
        f"=== STATISTICS REPORT ===\n"
        f"Data: {numbers}\n"
        f"Count: {len(numbers)} scores\n"
        f"Mean: {stats['mean']:.2f}\n"
        f"Median: {stats['median']:.2f}\n"
        f"Mode: {stats['mode']}\n"
        f"Range: {stats['range']} ({min(numbers)} to {max(numbers)})\n"
        f"Std Dev: {stats['std_dev']:.2f}\n"
    )

def process_statistics_functional(numbers):
    """Main functional processing pipeline"""
    start_time = time.time()

    # Pure functional composition pipeline
    stats = calculate_all_stats(numbers)
    report = format_report(numbers, stats)
    print(report)

    end_time = time.time()
    print(f"Functional processing time: {end_time - start_time:.4f} seconds")

# Test functional implementation
if __name__ == "__main__":
    test_scores = [85, 92, 78, 90, 88, 76, 95, 82, 87, 91]
    #test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 82, 87, 82, 91]
    #test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 87, 82, 91]
    process_statistics_functional(test_scores)
