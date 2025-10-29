import time
import math

# Global variables for storing results
stats_cache = {}

def calculate_mean(numbers):
    """Calculate arithmetic mean"""
    # TODO: Return sum of numbers divided by count
    pass

def calculate_median(numbers):
    """Calculate median value"""
    # TODO: Sort numbers and find middle value(s)
    pass

def find_mode(numbers):
    """Find most frequent number"""
    # TODO: Count frequencies and find most common
    # Return "No mode" if all numbers appear once
    pass

def calculate_range(numbers):
    """Calculate range (max - min)"""
    # TODO: Return difference between max and min
    pass

def calculate_std_dev(numbers):
    """Calculate standard deviation"""
    # TODO: Use formula: sqrt(sum((x - mean)²) / n)
    pass

def generate_stats_report(numbers):
    """Generate complete statistics report"""
    global stats_cache
    
    # TODO: Calculate all statistics
    # TODO: Format and print report
    # TODO: Store results in global stats_cache
    pass

def process_statistics_procedural(numbers):
    """Main procedural processing function"""
    start_time = time.time()
    
    generate_stats_report(numbers)
    
    end_time = time.time()
    print(f"Procedural processing time: {end_time - start_time:.4f} seconds")

# Test data
test_scores = [85, 92, 78, 90, 88, 76, 95, 82, 87, 91]

if __name__ == "__main__":
    process_statistics_procedural(test_scores)
