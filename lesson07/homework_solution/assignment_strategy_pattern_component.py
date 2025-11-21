from abc import ABC, abstractmethod
import time
from typing import List, Any

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[Any]) -> List[Any]:
        """Sort the data and return sorted list"""
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Return strategy name for reporting"""
        pass

class DataProcessor:
    def __init__(self, strategy: SortingStrategy = None):
        # TODO: Initialize with strategy
        pass
    
    def set_strategy(self, strategy: SortingStrategy):
        # TODO: Set the sorting strategy
        pass
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Use strategy to sort data
        pass
