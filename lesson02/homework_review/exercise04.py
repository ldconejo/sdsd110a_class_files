# Cache-unfriendly matrix multiplication
# Because of how Python lists are stored, elements in the same column of B are
# far apart in memory, causing many cache misses.

import random
import time

def matrix_multiply_bad(A, B, n):
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                # B[k][j] access pattern causes cache misses
                C[i][j] += A[i][k] * B[k][j]
    return C

if __name__ == "__main__":
    n = 256  # You can change this to 128, 256, 512 for testing
    random.seed(0)

    # Generate two random n×n matrices
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]

    # Run and time the naive version
    start = time.perf_counter()
    C1 = matrix_multiply_bad(A, B, n)
    end = time.perf_counter()
    print(f"Naive version: {end - start:.3f} seconds")

# list1 [[0, 2, 4, 2, 1, 5][2, 3, 5, 2, 1, 0]]