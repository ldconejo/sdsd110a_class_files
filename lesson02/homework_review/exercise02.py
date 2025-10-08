import random

# Random access causes cache misses
data = list(range(1000000))
indices = list(range(1000000))
random.shuffle(indices)

# Accessing data in random order
result = 0
for i in indices:
    result += data[i] * 2
