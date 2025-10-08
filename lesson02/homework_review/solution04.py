# Cache-unfriendly matrix multiplication
# Because of how Python lists are stored, elements in the same column of B are
# far apart in memory, causing many cache misses.

import random
import time

def matrix_multiply_transposed(A, B, n):
    # Transpose B so its columns become rows
    B_T = [[B[j][i] for j in range(n)] for i in range(n)]

    C = [[0.0] * n for _ in range(n)]
    for i in range(n):
        A_row = A[i]
        for j in range(n):
            B_row = B_T[j]
            total = 0.0
            for k in range(n):
                total += A_row[k] * B_row[k]
            C[i][j] = total
    return C

if __name__ == "__main__":
    n = 256  # You can change this to 128, 256, 512 for testing
    random.seed(0)

    # Generate two random n×n matrices
    A = [[random.random() for _ in range(n)] for _ in range(n)]
    B = [[random.random() for _ in range(n)] for _ in range(n)]

    # Run and time the naive version
    start = time.perf_counter()
    C1 = matrix_multiply_transposed(A, B, n)
    end = time.perf_counter()
    print(f"Transposed version: {end - start:.3f} seconds")