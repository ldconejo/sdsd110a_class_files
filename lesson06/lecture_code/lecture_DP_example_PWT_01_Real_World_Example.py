from abc import ABC, abstractmethod
from datetime import datetime

# Combine Observer + Strategy + Adapter patterns
class EventProcessor:
    """Combines multiple patterns for flexible event handling"""
    
    def __init__(self):
        self.observers = []
        self.processing_strategy = None
    
    # Observer pattern methods
    def subscribe(self, observer):
        self.observers.append(observer)
    
    def unsubscribe(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self, event):
        for observer in self.observers:
            observer.handle_event(event)
    
    # Strategy pattern methods
    def set_processing_strategy(self, strategy):
        self.processing_strategy = strategy
    
    def process_event(self, event):
        if self.processing_strategy:
            processed_event = self.processing_strategy.process(event)
            self.notify_observers(processed_event)
        else:
            self.notify_observers(event)

# Strategy for different event processing
class EventProcessingStrategy(ABC):
    @abstractmethod
    def process(self, event):
        pass

class SimpleEventProcessor(EventProcessingStrategy):
    def process(self, event):
        event["processed_by"] = "SimpleProcessor"
        event["timestamp"] = datetime.now()
        return event

class EnrichedEventProcessor(EventProcessingStrategy):
    def process(self, event):
        event["processed_by"] = "EnrichedProcessor"
        event["timestamp"] = datetime.now()
        event["metadata"] = {"enriched": True, "version": "1.0"}
        return event

# Observer implementations
class DatabaseLogger:
    def handle_event(self, event):
        print(f"DB: Logging event {event['type']} to database")

class EmailNotifier:
    def handle_event(self, event):
        if event['priority'] == 'high':
            print(f"EMAIL: Sending alert for {event['type']}")

class MetricsCollector:
    def handle_event(self, event):
        print(f"METRICS: Incrementing counter for {event['type']}")

# Adapter for legacy notification system
class LegacyNotificationAdapter:
    def __init__(self, legacy_system):
        self.legacy_system = legacy_system
    
    def handle_event(self, event):
        # Adapt new event format to legacy system format
        legacy_format = {
            "message": f"Event: {event['type']}",
            "level": event.get('priority', 'normal'),
            "source": "EventProcessor"
        }
        self.legacy_system.send_notification(legacy_format)

class LegacyNotificationSystem:
    def send_notification(self, notification):
        print(f"LEGACY: {notification['level'].upper()} - {notification['message']}")

# Usage - all patterns working together
processor = EventProcessor()

# Set up observers
processor.subscribe(DatabaseLogger())
processor.subscribe(EmailNotifier())
processor.subscribe(MetricsCollector())

# Add legacy system through adapter
legacy_system = LegacyNotificationSystem()
legacy_adapter = LegacyNotificationAdapter(legacy_system)
processor.subscribe(legacy_adapter)

# Set processing strategy
processor.set_processing_strategy(EnrichedEventProcessor())

# Process events
events = [
    {"type": "user_login", "user_id": "123", "priority": "normal"},
    {"type": "payment_failed", "amount": 99.99, "priority": "high"},
    {"type": "data_backup", "size": "2GB", "priority": "low"}
]

print("=== Event Processing System Demo ===")
for event in events:
    print(f"\nProcessing event: {event['type']}")
    processor.process_event(event)
