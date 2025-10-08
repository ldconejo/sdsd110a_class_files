# All x's are stored in a single array, making summation more efficient.
from array import array

x = array('d', (i for i in range(1_000_000)))
y = array('d', (i + 1 for i in range(1_000_000)))
z = array('d', (i + 2 for i in range(1_000_000)))

sum_x = sum(x)
