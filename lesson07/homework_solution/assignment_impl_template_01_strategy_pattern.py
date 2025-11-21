import time
import random
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
        # TODO: Implement bubble sort algorithm
        # Hint: Compare adjacent elements and swap if needed
        # Return sorted copy of data (don't modify original)
        pass
    
    def get_name(self) -> str:
        return "Bubble Sort"

class QuickSortStrategy(SortingStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        # TODO: Implement quicksort algorithm
        # Hint: Choose pivot, partition, recursively sort subarrays
        # Return sorted copy of data
        pass
    
    def get_name(self) -> str:
        return "Quick Sort"

class MergeSortStrategy(SortingStrategy):
    def sort(self, data: List[Any]) -> List[Any]:
        # TODO: Implement merge sort algorithm
        # Hint: Divide into halves, recursively sort, merge results
        # Return sorted copy of data
        pass
    
    def get_name(self) -> str:
        return "Merge Sort"

class DataProcessor:
    def __init__(self, strategy: SortingStrategy = None):
        # TODO: Store the strategy
        pass
    
    def set_strategy(self, strategy: SortingStrategy):
        # TODO: Update the current strategy
        pass
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Validate strategy exists and use it to sort data
        pass
