import time
import random
users = {i: {"name": f"user_{i}", "data": [0] * 100} for i in range(10000)}

def find_user_good(user_id):
    return users.get(user_id, None)
# O(1) average lookup time and better cache usage
# O(1) refers to "order one", meaning that the time taken is constant

start = time.perf_counter()
user = find_user_good(random.randint(0, 9999))
end = time.perf_counter()
print(f"Optimized version: {end - start:.6f} seconds")