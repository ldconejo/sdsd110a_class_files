import time
import math
from collections import Counter

class StatisticsCalculator:
    def __init__(self, data):
        self.data = data.copy()  # Defensive copy
        self.results = {}        # Store calculated results
    
    def calculate_mean(self):
        """Calculate and store mean"""
        mean = sum(self.data) / len(self.data)
        self.results['mean'] = mean
        return mean
    
    def calculate_median(self):
        """Calculate and store median"""
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        median = (sorted_data[mid - 1] + sorted_data[mid]) / 2 if n % 2 == 0 else sorted_data[mid]
        self.results['median'] = median
        return median
    
    def find_mode(self):
        """Find and store mode"""
        counts = Counter(self.data)
        max_count = max(counts.values())
        modes = [num for num, count in counts.items() if count == max_count]
        mode = modes[0] if len(modes) == 1 else modes
        if max_count == 1:
            mode = "No mode (all scores unique)"
        self.results['mode'] = mode
        return mode
    
    def calculate_range(self):
        """Calculate and store range"""
        data_range = max(self.data) - min(self.data)
        self.results['range'] = data_range
        return data_range
    
    def calculate_std_dev(self):
        """Calculate and store standard deviation"""
        mean = self.results.get('mean') or self.calculate_mean()
        variance = sum((x - mean) ** 2 for x in self.data) / len(self.data)
        std_dev = math.sqrt(variance)
        self.results['std_dev'] = std_dev
        return std_dev
    
    def calculate_all(self):
        """Calculate all statistics"""
        self.calculate_mean()
        self.calculate_median()
        self.find_mode()
        self.calculate_range()
        self.calculate_std_dev()
        return self.get_results()
    
    def get_results(self):
        """Return copy of results"""
        return self.results.copy()
    
    def generate_report(self):
        """Generate formatted report"""
        stats = self.get_results()
        report = (
            f"=== STATISTICS REPORT ===\n"
            f"Data: {self.data}\n"
            f"Count: {len(self.data)} scores\n"
            f"Mean: {stats['mean']:.2f}\n"
            f"Median: {stats['median']:.2f}\n"
            f"Mode: {stats['mode']}\n"
            f"Range: {stats['range']} ({min(self.data)} to {max(self.data)})\n"
            f"Std Dev: {stats['std_dev']:.2f}\n"
        )
        print(report)

def process_statistics_oop(numbers):
    """Main OOP processing function"""
    start_time = time.time()
    
    calculator = StatisticsCalculator(numbers)
    calculator.calculate_all()
    calculator.generate_report()
    
    end_time = time.time()
    print(f"OOP processing time: {end_time - start_time:.4f} seconds")

# Test the OOP implementation
if __name__ == "__main__":
    test_scores = [85, 92, 78, 90, 88, 76, 95, 82, 87, 91]
    #test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 82, 87, 82, 91]
    #test_scores = [85, 82, 92, 78, 90, 88, 76, 90, 90, 95, 82, 87, 82, 91]
    process_statistics_oop(test_scores)
