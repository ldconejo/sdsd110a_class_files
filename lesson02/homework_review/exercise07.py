# Multiple memory reallocations as list grows
def process_data_bad(data):
    result = []
    for item in data:
        if item % 2 == 0:
            # List may need to reallocate memory
            result.append(item * 2)
    return result

large_data = range(1000000)
processed = process_data_bad(large_data)
