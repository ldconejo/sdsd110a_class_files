import time

def build_string_good(data):
    # Convert all items to strings first
    # join() does all concatenation in one linear pass
    return ", ".join(str(item) for item in data)

# Memory allocation grows quadratically
large_data = range(10000000)

start = time.perf_counter()
output = build_string_good(large_data)
end = time.perf_counter()
print(f"Naive version: {end - start:.3f} seconds")