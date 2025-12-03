import time
import random
from collections import OrderedDict
from typing import Optional, Dict, List

class Database:
    """Simulates a slow database"""
    
    def __init__(self):
        # Create sample user data
        self.users = {
            f"user_{i}": {
                'name': f'User {i}',
                'email': f'user{i}@example.com',
                'data': f'Profile data for user {i}' * 5
            }
            for i in range(200)
        }
        self.query_count = 0
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user data (slow operation)"""
        self.query_count += 1
        time.sleep(0.005)  # Simulate 5ms database query
        return self.users.get(user_id)
    
    def reset_stats(self):
        self.query_count = 0

class LRUCache:
    """Least Recently Used cache implementation"""
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()
        self.hits = 0
        self.misses = 0
    
    def get(self, key: str) -> Optional[Dict]:
        """Get item from cache"""
        # TODO: Implement cache get logic
        # If key exists: record hit, move to end, return value
        # If key doesn't exist: record miss, return None
        
        if key in self.cache:
            # Cache hit - move to end and return
            self.hits += 1
            value = self.cache.pop(key)
            self.cache[key] = value  # Move to end
            return value
        else:
            # Cache miss
            self.misses += 1
            return None
    
    def put(self, key: str, value: Dict):
        """Put item in cache"""
        # TODO: Implement cache put logic
        # If at capacity: remove oldest item first
        # Add new item to end
        
        if key in self.cache:
            # Update existing - remove and re-add
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # Remove oldest (first item)
            self.cache.popitem(last=False)
        
        # Add to end (most recent)
        self.cache[key] = value
    
    def hit_ratio(self) -> float:
        """Calculate cache hit percentage"""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0
    
    def clear_stats(self):
        """Reset hit/miss counters"""
        self.hits = 0
        self.misses = 0

class WebApplication:
    """Simulates a web application that serves user profiles"""
    
    def __init__(self, use_cache: bool = False, cache_size: int = 50):
        self.database = Database()
        self.use_cache = use_cache
        self.cache = LRUCache(cache_size) if use_cache else None
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile (with optional caching)"""
        
        if self.use_cache:
            # TODO: Implement cached lookup
            # Check cache first, if miss then get from database and cache result
            
            # Check cache first
            user_data = self.cache.get(user_id)
            if user_data is not None:
                return user_data
            
            # Cache miss - get from database
            user_data = self.database.get_user(user_id)
            if user_data:
                self.cache.put(user_id, user_data)
            
            return user_data
        else:
            # No cache - direct database access
            return self.database.get_user(user_id)

class PerformanceTester:
    """Tests and compares application performance"""
    
    def generate_user_requests(self, num_requests: int = 500) -> List[str]:
        """Generate realistic user request pattern"""
        # TODO: Create request pattern where some users are accessed more frequently
        # 80% of requests should go to 20% of users (popular users)
        
        requests = []
        popular_users = [f"user_{i}" for i in range(40)]  # 20% of users
        regular_users = [f"user_{i}" for i in range(40, 200)]  # 80% of users
        
        for _ in range(num_requests):
            if random.random() < 0.8:  # 80% chance
                user_id = random.choice(popular_users)
            else:  # 20% chance
                user_id = random.choice(regular_users)
            requests.append(user_id)
        
        return requests
    
    def test_performance(self, use_cache: bool, requests: List[str]) -> Dict:
        """Test application performance"""
        
        app = WebApplication(use_cache=use_cache, cache_size=50)
        
        print(f"Testing {'WITH' if use_cache else 'WITHOUT'} cache...")
        
        # Reset database stats
        app.database.reset_stats()
        if app.cache:
            app.cache.clear_stats()
        
        # Time the requests
        start_time = time.time()
        
        for user_id in requests:
            profile = app.get_user_profile(user_id)
        
        end_time = time.time()
        
        # Gather results
        results = {
            'cached': use_cache,
            'total_time': end_time - start_time,
            'database_queries': app.database.query_count,
            'requests_served': len(requests)
        }
        
        if app.cache:
            results['hit_ratio'] = app.cache.hit_ratio()
            results['cache_hits'] = app.cache.hits
            results['cache_misses'] = app.cache.misses
        
        return results
    
    def run_comparison(self):
        """Run performance comparison"""
        
        print("CACHE PERFORMANCE COMPARISON")
        print("=" * 50)
        
        # Generate request pattern
        requests = self.generate_user_requests(500)
        unique_users = len(set(requests))
        
        print(f"Generated {len(requests)} requests for {unique_users} unique users")
        
        # Test without cache
        no_cache_results = self.test_performance(False, requests)
        
        # Test with cache  
        cache_results = self.test_performance(True, requests)
        
        # Print results
        self.print_comparison(no_cache_results, cache_results)
        
        return no_cache_results, cache_results
    
    def print_comparison(self, no_cache: Dict, with_cache: Dict):
        """Print formatted comparison results"""
        
        print(f"\nRESULTS:")
        print("-" * 40)
        
        print(f"WITHOUT Cache:")
        print(f"  Time taken: {no_cache['total_time']:.3f} seconds")
        print(f"  Database queries: {no_cache['database_queries']}")
        
        print(f"\nWITH Cache:")
        print(f"  Time taken: {with_cache['total_time']:.3f} seconds")
        print(f"  Database queries: {with_cache['database_queries']}")
        print(f"  Cache hit ratio: {with_cache['hit_ratio']:.1f}%")
        print(f"  Cache hits: {with_cache['cache_hits']}")
        print(f"  Cache misses: {with_cache['cache_misses']}")
        
        # Calculate improvements
        if no_cache['total_time'] > 0:
            speedup = no_cache['total_time'] / with_cache['total_time']
            query_reduction = (1 - with_cache['database_queries'] / no_cache['database_queries']) * 100
            
            print(f"\nIMPROVEMENT:")
            print(f"  Speed improvement: {speedup:.1f}x faster")
            print(f"  Database queries reduced by: {query_reduction:.1f}%")

def analyze_caching_scenarios():
    """Analyze when to use caching"""
    
    print(f"\n" + "=" * 50)
    print("CACHING SCENARIO ANALYSIS")
    print("=" * 50)
    
    scenarios = [
        {
            'name': 'News Website',
            'pattern': 'Few popular articles get most traffic',
            'cache_benefit': 'High - popular articles cached',
            'recommended': 'Yes - LRU cache for articles'
        },
        {
            'name': 'Banking System',
            'pattern': 'Account data changes frequently',
            'cache_benefit': 'Low - data changes too often',
            'recommended': 'Limited - only for reference data'
        },
        {
            'name': 'Social Media Feed',
            'pattern': 'Recent posts accessed repeatedly',
            'cache_benefit': 'High - recent content popular',
            'recommended': 'Yes - cache recent posts and user data'
        },
        {
            'name': 'E-commerce Catalog',
            'pattern': 'Popular products viewed often',
            'cache_benefit': 'High - product info rarely changes',
            'recommended': 'Yes - cache product details and images'
        }
    ]
    
    print("Scenario Analysis:")
    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print(f"  Access Pattern: {scenario['pattern']}")
        print(f"  Cache Benefit: {scenario['cache_benefit']}")
        print(f"  Recommendation: {scenario['recommended']}")

def main():
    """Run the complete assignment"""
    
    # Run performance tests
    tester = PerformanceTester()
    no_cache_results, cache_results = tester.run_comparison()
    
    # Analyze scenarios
    analyze_caching_scenarios()
    
    print(f"\n" + "=" * 50)
    print("ASSIGNMENT QUESTIONS")
    print("=" * 50)
    print("Answer these questions in your report:")
    print("1. How much faster was the cached version?")
    print("2. What was the cache hit ratio and why?")
    print("3. How many database queries were avoided?")
    print("4. Which scenarios would benefit most from caching?")
    print("5. What happens if cache size is too small?")

if __name__ == "__main__":
    main()
