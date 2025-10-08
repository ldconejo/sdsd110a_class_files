import time
# Creates new string objects repeatedly
def build_string_bad(data):
    result = ""
    for item in data:
        # Each += creates a new string object
        result += str(item) + ", "
    return result

# Memory allocation grows quadratically
large_data = range(10000000)

start = time.perf_counter()
output = build_string_bad(large_data)
end = time.perf_counter()
print(f"Naive version: {end - start:.3f} seconds")