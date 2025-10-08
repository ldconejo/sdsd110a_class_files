import random

data = list(range(1000000))
indices = list(range(1000000))
random.shuffle(indices)

# Note that, in the end, you still have to access all elements,
# so you don't gain anything by adding in the order stated by indices.
result = sum(x * 2 for x in data)

