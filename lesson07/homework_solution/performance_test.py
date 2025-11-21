import time
from datetime import datetime
from typing import List, Any
from abc import ABC
from data_processor import SortingStrategy

class ProcessorDecorator(ABC):
    def __init__(self, processor):
        self._processor = processor
    
    def process(self, data: List[Any]) -> List[Any]:
        return self._processor.process(data)
    
    def set_strategy(self, strategy: SortingStrategy):
        self._processor.set_strategy(strategy)

    def __getattr__(self, name):
        # Forward unknown attributes/methods to inner processor
        return getattr(self._processor, name)

class TimingDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.execution_times = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Record start time, process data, record end time
        start = time.perf_counter()
        result = self._processor.process(data)
        end = time.perf_counter()

        # Store execution time
        execution_time = end - start
        self.execution_times.append(execution_time)

        # Print timing info
        print(f"[TimingDecorator] Execution time: {execution_time:.6f} seconds")

        return result
    
    def get_average_time(self):
        # TODO: Return average execution time
        if not self.execution_times:
            return 0.0
        return sum(self.execution_times) / len(self.execution_times)
    
    def reset(self):
        self.execution_times = []

class LoggingDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.log_entries = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Log operation details (data size, timestamp)
        start_log = f"[LoggingDecorator] Start: size={len(data)}, time={datetime.now()}"
        self.log_entries.append(start_log)
        print(start_log)

        # Process the data
        result = self._processor.process(data)

        # Log completion
        end_log = f"[LoggingDecorator] End: size={len(result)}, time={datetime.now()}"
        self.log_entries.append(end_log)
        print(end_log)

        return result
    
    def get_logs(self):
        # TODO: Return log entries
        return self.log_entries

class ValidationDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.validation_errors = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Validate input data (check if list, not empty, etc.)
        if not isinstance(data, list):
            error = "Input must be a list."
            self.validation_errors.append(error)
            raise ValueError(error)

        if len(data) == 0:
            error = "Input list cannot be empty."
            self.validation_errors.append(error)
            raise ValueError(error)

        # Process the data
        result = self._processor.process(data)

        # Validate output (check if sorted correctly)
        if not self.is_sorted(result):
            error = "Output data is not sorted correctly."
            self.validation_errors.append(error)
            raise ValueError(error)

        print("[ValidationDecorator] Data successfully validated and sorted.")
        return result
    
    def is_sorted(self, data: List[Any]) -> bool:
        # TODO: Check if data is sorted correctly
        return all(data[i] <= data[i + 1] for i in range(len(data) - 1))
