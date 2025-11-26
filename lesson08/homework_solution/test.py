import time
from assignment_solution import TaskQueueSystem, EmailTask, ImageProcessingTask

def test_your_system():
    """Test script to verify your implementation"""
    print("🧪 Testing Task Queue System")
    
    # Create system
    system = TaskQueueSystem(num_workers=3, max_queue_size=10)
    
    # Submit various tasks
    system.submit_task(EmailTask("user1@example.com", "Welcome"))
    system.submit_task(ImageProcessingTask("photo1.jpg", "resize"))
    system.submit_task(EmailTask("user2@example.com", "Newsletter"))
    system.submit_task(ImageProcessingTask("photo2.jpg", "crop"))
    
    # Let tasks process
    time.sleep(3)
    
    # Check statistics
    stats = system.get_stats()
    print(f"System stats: {stats}")
    
    # Shutdown
    system.shutdown()

if __name__ == "__main__":
    test_your_system()