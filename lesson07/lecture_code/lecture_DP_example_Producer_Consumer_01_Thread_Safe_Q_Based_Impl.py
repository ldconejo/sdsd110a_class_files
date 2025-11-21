import threading
import queue
import time
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class WorkItem:
    id: int
    data: str
    created_at: float
    priority: int = 1

class Producer(threading.Thread):
    def __init__(self, work_queue: queue.Queue, producer_id: int, item_count: int):
        super().__init__()
        self.work_queue = work_queue
        self.producer_id = producer_id
        self.item_count = item_count
        self.daemon = True
    
    def run(self):
        """Producer thread main loop"""
        for i in range(self.item_count):
            # Simulate work to generate data
            time.sleep(random.uniform(0.1, 0.5))
            
            # Create work item
            work_item = WorkItem(
                id=i,
                data=f"Data from Producer {self.producer_id}, item {i}",
                created_at=time.time(),
                priority=random.randint(1, 5)
            )
            
            try:
                # Add to queue (blocks if queue is full)
                self.work_queue.put(work_item, timeout=2)
                print(f"📦 Producer {self.producer_id} created item {i}")
            except queue.Full:
                print(f"⚠️  Producer {self.producer_id} queue full, dropping item {i}")
        
        print(f"✅ Producer {self.producer_id} finished")

class Consumer(threading.Thread):
    def __init__(self, work_queue: queue.Queue, consumer_id: int):
        super().__init__()
        self.work_queue = work_queue
        self.consumer_id = consumer_id
        self.processed_count = 0
        self.daemon = True
        self.shutdown_event = threading.Event()
    
    def run(self):
        """Consumer thread main loop"""
        while not self.shutdown_event.is_set():
            try:
                # Get work item from queue
                work_item = self.work_queue.get(timeout=1)
                
                # Process the work item
                self.process_item(work_item)
                
                # Mark task as done
                self.work_queue.task_done()
                
            except queue.Empty:
                # No work available, continue checking
                continue
        
        print(f"🏁 Consumer {self.consumer_id} processed {self.processed_count} items")
    
    def process_item(self, item: WorkItem):
        """Process a single work item"""
        # Simulate processing time based on priority
        processing_time = 0.1 * item.priority
        time.sleep(processing_time)
        
        self.processed_count += 1
        age = time.time() - item.created_at
        
        print(f"⚙️  Consumer {self.consumer_id} processed item {item.id} "
              f"(age: {age:.2f}s, priority: {item.priority})")
    
    def shutdown(self):
        """Signal consumer to shutdown"""
        self.shutdown_event.set()

# Producer-Consumer Coordinator
class WorkflowManager:
    def __init__(self, queue_size=10):
        self.work_queue = queue.Queue(maxsize=queue_size)
        self.producers = []
        self.consumers = []
    
    def add_producer(self, producer_id: int, item_count: int):
        """Add a producer thread"""
        producer = Producer(self.work_queue, producer_id, item_count)
        self.producers.append(producer)
        return producer
    
    def add_consumer(self, consumer_id: int):
        """Add a consumer thread"""
        consumer = Consumer(self.work_queue, consumer_id)
        self.consumers.append(consumer)
        return consumer
    
    def start_all(self):
        """Start all producers and consumers"""
        print("🚀 Starting workflow...")
        
        # Start consumers first
        for consumer in self.consumers:
            consumer.start()
        
        # Start producers
        for producer in self.producers:
            producer.start()
    
    def wait_for_completion(self):
        """Wait for all work to complete"""
        # Wait for all producers to finish
        for producer in self.producers:
            producer.join()
        
        print("📋 All producers finished, waiting for queue to empty...")
        
        # Wait for queue to be empty
        self.work_queue.join()
        
        print("✅ All work completed, shutting down consumers...")
        
        # Shutdown consumers
        for consumer in self.consumers:
            consumer.shutdown()
            consumer.join(timeout=2)
    
    def get_stats(self):
        """Get workflow statistics"""
        return {
            "queue_size": self.work_queue.qsize(),
            "producers": len(self.producers),
            "consumers": len(self.consumers),
            "total_processed": sum(c.processed_count for c in self.consumers)
        }

# Usage Example
def demonstrate_producer_consumer():
    # Create workflow manager
    manager = WorkflowManager(queue_size=5)
    
    # Add 2 producers, each creating 10 items
    manager.add_producer(producer_id=1, item_count=10)
    manager.add_producer(producer_id=2, item_count=10)
    
    # Add 3 consumers to process the work
    manager.add_consumer(consumer_id=1)
    manager.add_consumer(consumer_id=2)
    manager.add_consumer(consumer_id=3)
    
    # Start the workflow
    manager.start_all()
    
    # Wait for completion
    manager.wait_for_completion()
    
    # Print final stats
    print("\n📊 Final Statistics:")
    stats = manager.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    demonstrate_producer_consumer()