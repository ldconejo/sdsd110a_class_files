import time
import math
from collections import Counter

class StatisticsCalculator:
    def __init__(self, data):
        self.data = data.copy()  # Store copy of data
        self.results = {}        # Store calculated results
    
    def calculate_mean(self):
        """Calculate and store mean"""
        # TODO: Calculate mean and store in self.results['mean']
        pass
    
    def calculate_median(self):
        """Calculate and store median"""
        # TODO: Calculate median and store in self.results['median']
        pass
    
    def find_mode(self):
        """Find and store mode"""
        # TODO: Find mode and store in self.results['mode']
        pass
    
    def calculate_range(self):
        """Calculate and store range"""
        # TODO: Calculate range and store in self.results['range']
        pass
    
    def calculate_std_dev(self):
        """Calculate and store standard deviation"""
        # TODO: Calculate std dev and store in self.results['std_dev']
        pass
    
    def calculate_all(self):
        """Calculate all statistics"""
        # TODO: Call all calculation methods
        pass
    
    def get_results(self):
        """Return copy of results"""
        return self.results.copy()
    
    def generate_report(self):
        """Generate formatted report"""
        # TODO: Print formatted statistics report
        pass

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
    process_statistics_oop(test_scores)
