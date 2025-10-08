results = [0] * 100000
temp = [0] * 100  # Reuse same list every iteration

for i in range(100000):
    for j in range(100):
        temp[j] = i * j
    results[i] = sum(temp)
