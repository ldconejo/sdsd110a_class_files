from multiprocessing import Pool

def square(x):
    return x * x

# Process list in parallel across CPU cores
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    with Pool() as pool:
        results = pool.map(square, numbers)
        print(results)  # [1, 4, 9, 16, 25, 36, 49, 64]
