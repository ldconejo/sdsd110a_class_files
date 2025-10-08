# Excessive function call overhead
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def process_bad(data):
    result = 0
    for i in range(len(data)):
        # Many function calls with overhead
        temp = add(data[i], 1)
        result = add(result, multiply(temp, 2))
    return result

data = list(range(100000))
result = process_bad(data)
