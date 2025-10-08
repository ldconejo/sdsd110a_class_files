def process_good(data):
    result = 0
    for i in range(len(data)):
        result += (data[i] + 1) * 2
    return result

data = list(range(100000))
result = process_good(data)
