def process_data_good(data):
    return [item * 2 for item in data if item % 2 == 0]
# List comprehension builds the list in one pass with better memory usage

large_data = range(1000000)
processed = process_data_good(large_data)
