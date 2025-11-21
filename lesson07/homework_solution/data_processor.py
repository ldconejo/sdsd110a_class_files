from typing import List, Any
from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[Any]) -> List[Any]:
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        pass

class BubbleSortStrategy(SortingStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr
    
    def get_name(self) -> str:
        return "Bubble Sort"

class QuickSortStrategy(SortingStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        arr = data.copy()

        def quicksort(a):
            if len(a) <= 1:
                return a
            pivot = a[len(a) // 2]
            left = [x for x in a if x < pivot]
            middle = [x for x in a if x == pivot]
            right = [x for x in a if x > pivot]
            return quicksort(left) + middle + quicksort(right)

        return quicksort(arr)
    
    def get_name(self) -> str:
        return "Quick Sort"

class MergeSortStrategy(SortingStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        arr = data.copy()

        def mergesort(a):
            if len(a) <= 1:
                return a
            
            mid = len(a) // 2
            left = mergesort(a[:mid])
            right = mergesort(a[mid:])
            
            return merge(left, right)

        def merge(left, right):
            result = []
            i = j = 0
            
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            result.extend(left[i:])
            result.extend(right[j:])
            return result

        return mergesort(arr)
    
    def get_name(self) -> str:
        return "Merge Sort"

class DataProcessor:
    def __init__(self, strategy: SortingStrategy = None):
        # TODO: Store the strategy
        self.strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy):
        # TODO: Update the current strategy
        self.strategy = strategy
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Validate strategy exists and use it to sort data
        if not self.strategy:
            raise ValueError("No sorting strategy set.")
        return self.strategy.sort(data)
