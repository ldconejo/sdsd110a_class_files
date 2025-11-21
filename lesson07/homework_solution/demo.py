import random
from typing import List, Dict, Any
from data_processor import DataProcessor, QuickSortStrategy, MergeSortStrategy, BubbleSortStrategy, SortingStrategy
from performance_test import TimingDecorator, LoggingDecorator, ValidationDecorator

def generate_test_data(size: int, data_type: str = "random") -> List[int]:
    """Generate test data for performance testing.
    data_type options: "random", "sorted", "reverse_sorted", "nearly_sorted"
    """
    if data_type == "random":
        return [random.randint(0, size) for _ in range(size)]

    elif data_type == "sorted":
        return list(range(size))

    elif data_type == "reverse_sorted":
        return list(range(size, 0, -1))

    elif data_type == "nearly_sorted":
        data = list(range(size))
        # make a few random swaps (5% of data)
        swaps = max(1, size // 20)
        for _ in range(swaps):
            i, j = random.randint(0, size - 1), random.randint(0, size - 1)
            data[i], data[j] = data[j], data[i]
        return data

    else:
        raise ValueError(f"Unknown data_type: {data_type}")


def run_performance_test(processor, data_sizes: List[int], strategies: List[SortingStrategy]) -> Dict[str, Any]:
    """Run performance tests across different data sizes and strategies.
       Returns a dict of timing results.
    """
    results = {}

    for strategy in strategies:
        strategy_name = strategy.get_name()
        results[strategy_name] = {}

        processor.set_strategy(strategy)

        for size in data_sizes:
            test_data = generate_test_data(size, "random")

            # Run processing
            processor.process(test_data)

            # Retrieve timing if available
            if hasattr(processor, "get_average_time"):
                avg_time = processor.get_average_time()
                processor.reset()
            else:
                avg_time = None

            results[strategy_name][size] = avg_time

    return results


def performance_analysis():
    """Analyze performance of different strategies with and without decorators."""
    strategies = [
        BubbleSortStrategy(),
        QuickSortStrategy(),
        MergeSortStrategy()
    ]

    data_sizes = [50, 200, 800]

    print("\n=== Running Performance Tests ===")

    # ---------- Without decorators ----------
    print("\n--- WITHOUT DECORATORS ---")
    base_processor = DataProcessor()
    results_plain = run_performance_test(
        processor=TimingDecorator(base_processor),
        data_sizes=data_sizes,
        strategies=strategies
    )

    # ---------- With decorators (Timing + Validation) ----------
    print("\n--- WITH DECORATORS (Timing + Logging + Validation) ---")
    decorated_processor = TimingDecorator(
        LoggingDecorator(
            ValidationDecorator(
                DataProcessor()
            )
        )
    )

    results_decorated = run_performance_test(
        processor=decorated_processor,
        data_sizes=data_sizes,
        strategies=strategies
    )

    # ---------- Print Results ----------
    print("\n=== PERFORMANCE SUMMARY ===")
    for strategy in results_plain:
        print(f"\nStrategy: {strategy}")

        for size in data_sizes:
            plain = results_plain[strategy][size]
            deco = results_decorated[strategy][size]

            plain_str = f"{plain:.6f}" if plain is not None else "N/A"
            deco_str  = f"{deco:.6f}" if deco  is not None else "N/A"

            print(f"  Size {size:4d} | "
                f"Raw: {plain_str} sec | "
                f"Decorated: {deco_str} sec")

    print("\nDone.")

if __name__ == "__main__":
    print("Starting performance analysis demo...\n")
    performance_analysis()

