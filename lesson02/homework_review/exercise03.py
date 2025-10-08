# Creating new objects in each iteration
results = []
for i in range(100000):
    # New list allocation each iteration
    temp = []
    for j in range(100):
        # This append triggers a resize occasionally 
        temp.append(i * j)
    results.append(sum(temp))
