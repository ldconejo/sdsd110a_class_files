class ProcessorDecorator(ABC):
    def __init__(self, processor):
        self._processor = processor
    
    def process(self, data: List[Any]) -> List[Any]:
        return self._processor.process(data)
    
    def set_strategy(self, strategy: SortingStrategy):
        self._processor.set_strategy(strategy)

class TimingDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.execution_times = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Record start time, process data, record end time
        # Store execution time in self.execution_times
        # Print timing information
        # Return the processed data
        pass
    
    def get_average_time(self):
        # TODO: Return average execution time
        pass

class LoggingDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.log_entries = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Log operation details (data size, timestamp)
        # Process the data
        # Log completion
        # Return processed data
        pass
    
    def get_logs(self):
        # TODO: Return log entries
        pass

class ValidationDecorator(ProcessorDecorator):
    def __init__(self, processor):
        super().__init__(processor)
        self.validation_errors = []
    
    def process(self, data: List[Any]) -> List[Any]:
        # TODO: Validate input data (check if list, not empty, etc.)
        # Process the data
        # Validate output (check if sorted correctly)
        # Return processed data or raise exception if validation fails
        pass
    
    def is_sorted(self, data: List[Any]) -> bool:
        # TODO: Check if data is sorted correctly
        pass
