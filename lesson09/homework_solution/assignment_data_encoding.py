import json
import pickle
import time
import matplotlib.pyplot as plt
from datetime import datetime
from typing import Any, Dict, List
try:
    import msgpack
except ImportError:
    print("Please install msgpack: pip install msgpack")
    exit(1)

class EncodingBenchmark:
    """Compare different encoding formats"""
    
    def __init__(self):
        self.results = {}
    
    def json_encode_decode(self, data: Any) -> tuple:
        """JSON encoding with datetime handling"""
        
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        # TODO: Implement JSON encoding and decoding
        # Measure time for encoding
        start_time = time.perf_counter()
        # encoded = ?  # Use json.dumps with the serializer above
        encode_time = time.perf_counter() - start_time
        
        # Measure time for decoding  
        start_time = time.perf_counter()
        # decoded = ?  # Use json.loads
        decode_time = time.perf_counter() - start_time
        
        return encoded, encode_time, decode_time
    
    def messagepack_encode_decode(self, data: Any) -> tuple:
        """MessagePack encoding"""
        
        # TODO: Implement MessagePack encoding and decoding
        # Measure time for encoding
        start_time = time.perf_counter()
        # encoded = ?  # Use msgpack.packb
        encode_time = time.perf_counter() - start_time
        
        # Measure time for decoding
        start_time = time.perf_counter()
        # decoded = ?  # Use msgpack.unpackb
        decode_time = time.perf_counter() - start_time
        
        return encoded, encode_time, decode_time
    
    def pickle_encode_decode(self, data: Any) -> tuple:
        """Pickle encoding"""
        
        # TODO: Implement Pickle encoding and decoding
        # Measure time for encoding
        start_time = time.perf_counter()
        # encoded = ?  # Use pickle.dumps
        encode_time = time.perf_counter() - start_time
        
        # Measure time for decoding
        start_time = time.perf_counter()
        # decoded = ?  # Use pickle.loads
        decode_time = time.perf_counter() - start_time
        
        return encoded, encode_time, decode_time
    
    def benchmark_data(self, dataset_name: str, data: Any):
        """Benchmark all formats on given data"""
        
        print(f"\nBenchmarking: {dataset_name}")
        print("-" * 40)
        
        formats = {
            'JSON': self.json_encode_decode,
            'MessagePack': self.messagepack_encode_decode,
            'Pickle': self.pickle_encode_decode
        }
        
        results = {}
        
        for format_name, encode_decode_func in formats.items():
            try:
                encoded, encode_time, decode_time = encode_decode_func(data)
                
                results[format_name] = {
                    'size_bytes': len(encoded),
                    'encode_time_ms': encode_time * 1000,
                    'decode_time_ms': decode_time * 1000,
                    'total_time_ms': (encode_time + decode_time) * 1000
                }
                
                print(f"{format_name:12} | {len(encoded):8,} bytes | "
                      f"{encode_time*1000:6.2f}ms encode | {decode_time*1000:6.2f}ms decode")
                
            except Exception as e:
                print(f"{format_name:12} | ERROR: {str(e)}")
                results[format_name] = None
        
        self.results[dataset_name] = results
        return results

def create_test_datasets():
    """Create test datasets of varying complexity"""
    
    # TODO: Create three different datasets
    
    # Dataset 1: Simple user data
    simple_user = {
        # TODO: Add user fields like id, name, email, age, active status
    }
    
    # Dataset 2: Complex nested user data  
    complex_user = {
        # TODO: Add nested structure with profile, preferences, metadata
        # Include a datetime field to test JSON datetime handling
    }
    
    # Dataset 3: Large list of users
    user_list = [
        # TODO: Create list of 1000 simple user objects
        # Use list comprehension to generate users with different IDs
    ]
    
    return {
        'simple_user': simple_user,
        'complex_user': complex_user,
        'user_list': user_list
    }

def create_performance_chart(results: Dict):
    """Create visualization of benchmark results"""
    
    # TODO: Create a bar chart comparing the three formats
    # You can use the provided code below as a starting point
    
    datasets = list(results.keys())
    formats = ['JSON', 'MessagePack', 'Pickle']
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Size comparison
    for i, dataset in enumerate(datasets):
        sizes = []
        for format_name in formats:
            if results[dataset][format_name]:
                sizes.append(results[dataset][format_name]['size_bytes'])
            else:
                sizes.append(0)
        
        x_pos = [j + i*0.25 for j in range(len(formats))]
        ax1.bar(x_pos, sizes, width=0.25, label=dataset)
    
    ax1.set_xlabel('Format')
    ax1.set_ylabel('Size (bytes)')
    ax1.set_title('Encoding Size Comparison')
    ax1.set_xticks(range(len(formats)))
    ax1.set_xticklabels(formats)
    ax1.legend()
    
    # Time comparison  
    for i, dataset in enumerate(datasets):
        times = []
        for format_name in formats:
            if results[dataset][format_name]:
                times.append(results[dataset][format_name]['total_time_ms'])
            else:
                times.append(0)
        
        x_pos = [j + i*0.25 for j in range(len(formats))]
        ax2.bar(x_pos, times, width=0.25, label=dataset)
    
    ax2.set_xlabel('Format') 
    ax2.set_ylabel('Total Time (ms)')
    ax2.set_title('Encoding Speed Comparison')
    ax2.set_xticks(range(len(formats)))
    ax2.set_xticklabels(formats)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('encoding_performance.png')
    plt.show()

def analyze_results(results: Dict):
    """Analyze and summarize benchmark results"""
    
    print("\n" + "="*60)
    print("PERFORMANCE ANALYSIS SUMMARY")
    print("="*60)
    
    # TODO: Write analysis code to find:
    # 1. Which format is consistently smallest
    # 2. Which format is consistently fastest
    # 3. How performance changes with data complexity
    
    # Example analysis structure:
    print("\nSize Analysis:")
    # Your analysis here
    
    print("\nSpeed Analysis:")  
    # Your analysis here
    
    print("\nTrade-off Analysis:")
    # Your analysis here

def main():
    """Run the complete benchmark"""
    
    print("DATA ENCODING PERFORMANCE BENCHMARK")
    print("="*60)
    
    # Create benchmark instance
    benchmark = EncodingBenchmark()
    
    # Create test datasets
    datasets = create_test_datasets()
    
    # Run benchmarks
    for dataset_name, data in datasets.items():
        benchmark.benchmark_data(dataset_name, data)
    
    # Analyze results
    analyze_results(benchmark.results)
    
    # Create visualization
    create_performance_chart(benchmark.results)
    
    print(f"\nBenchmark complete! Check 'encoding_performance.png' for charts.")
    
    return benchmark.results

if __name__ == "__main__":
    results = main()
