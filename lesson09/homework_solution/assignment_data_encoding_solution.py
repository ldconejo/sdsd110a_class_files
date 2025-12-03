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
        
        start_time = time.perf_counter()
        encoded = json.dumps(data, default=json_serializer)
        encode_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        decoded = json.loads(encoded)
        decode_time = time.perf_counter() - start_time
        
        return encoded, encode_time, decode_time
    
    def messagepack_encode_decode(self, data: Any) -> tuple:
        """MessagePack encoding"""
        
        start_time = time.perf_counter()
        encoded = msgpack.packb(
            data,
            default=lambda obj: obj.isoformat() if isinstance(obj, datetime) else obj,
            use_bin_type=True
        )
        encode_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        decoded = msgpack.unpackb(encoded, raw=False)
        decode_time = time.perf_counter() - start_time
        
        return encoded, encode_time, decode_time
    
    def pickle_encode_decode(self, data: Any) -> tuple:
        """Pickle encoding"""
        
        start_time = time.perf_counter()
        encoded = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
        encode_time = time.perf_counter() - start_time
        
        start_time = time.perf_counter()
        decoded = pickle.loads(encoded)
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
    
    simple_user = {
        'id': 1,
        'name': 'Alice Example',
        'email': 'alice@example.com',
        'age': 29,
        'active': True
    }
    
    complex_user = {
        'profile': {
            'id': 42,
            'name': 'Bob Nested',
            'joined_at': datetime(2020, 5, 17, 10, 30),
            'roles': ['admin', 'editor']
        },
        'preferences': {
            'notifications': {
                'email': True,
                'sms': False,
                'push': True
            },
            'theme': 'solarized',
            'languages': ['en', 'es', 'fr']
        },
        'metadata': {
            'tags': ['beta', 'vip', 'imported'],
            'last_login': datetime.now(),
            'stats': {
                'logins': 153,
                'purchases': 12,
                'avg_session_seconds': 532.4
            }
        }
    }
    
    user_list = [
        {
            'id': i,
            'name': f'User {i}',
            'email': f'user{i}@example.com',
            'age': 18 + (i % 40),
            'active': i % 2 == 0
        }
        for i in range(1000)
    ]
    
    return {
        'simple_user': simple_user,
        'complex_user': complex_user,
        'user_list': user_list
    }

def create_performance_chart(results: Dict):
    """Create visualization of benchmark results"""
    
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
    
    print("\nSize Analysis:")
    format_names = ['JSON', 'MessagePack', 'Pickle']
    size_totals = {fmt: 0 for fmt in format_names}
    time_totals = {fmt: 0 for fmt in format_names}
    counts = {fmt: 0 for fmt in format_names}
    
    for dataset_name, dataset_results in results.items():
        available = {fmt: dataset_results.get(fmt) for fmt in format_names if dataset_results.get(fmt)}
        if not available:
            continue
        smallest_fmt = min(available, key=lambda f: available[f]['size_bytes'])
        print(f"{dataset_name}: smallest = {smallest_fmt} ({available[smallest_fmt]['size_bytes']} bytes)")
        for fmt, metrics in available.items():
            size_totals[fmt] += metrics['size_bytes']
            time_totals[fmt] += metrics['total_time_ms']
            counts[fmt] += 1
    
    print("\nSpeed Analysis:")  
    for dataset_name, dataset_results in results.items():
        available = {fmt: dataset_results.get(fmt) for fmt in format_names if dataset_results.get(fmt)}
        if not available:
            continue
        fastest_fmt = min(available, key=lambda f: available[f]['total_time_ms'])
        print(f"{dataset_name}: fastest = {fastest_fmt} ({available[fastest_fmt]['total_time_ms']:.2f} ms)")
    
    print("\nTrade-off Analysis:")
    overall_smallest = None
    overall_fastest = None
    if any(counts.values()):
        overall_smallest = min(
            (fmt for fmt in format_names if counts[fmt]),
            key=lambda f: size_totals[f] / counts[f]
        )
        overall_fastest = min(
            (fmt for fmt in format_names if counts[fmt]),
            key=lambda f: time_totals[f] / counts[f]
        )
        print(f"Overall smallest on average: {overall_smallest}")
        print(f"Overall fastest on average: {overall_fastest}")
    
    if all(key in results for key in ('simple_user', 'complex_user', 'user_list')):
        print("\nComplexity impact (relative to simple_user):")
        base = results['simple_user']
        for fmt in format_names:
            if base.get(fmt) and results['user_list'].get(fmt):
                size_growth = results['user_list'][fmt]['size_bytes'] / base[fmt]['size_bytes']
                time_growth = results['user_list'][fmt]['total_time_ms'] / base[fmt]['total_time_ms']
                print(f"{fmt}: size x{size_growth:.1f}, time x{time_growth:.1f}")

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
