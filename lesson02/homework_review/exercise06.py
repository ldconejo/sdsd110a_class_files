# O(n) lookup time and poor cache usage
# O(n) refers to "order n", meaning that the time taken grows linearly
# with the number of users. This is inefficient for large datasets.
import time
import random
users = []
for i in range(10000):
    users.append({"id": i, "name": f"user_{i}", "data": [0] * 100})

# Frequent lookups are slow
def find_user_bad(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
        return None
        
start = time.perf_counter()
user = find_user_bad(9999)
end = time.perf_counter()
print(f"Naive version: {end - start:.6f} seconds")
