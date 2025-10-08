import random

class DataPoint:
    # Using __slots__ to reduce memory overhead (no __dict__ per object)
    # Numeric attributes grouped together for better cache locality
    __slots__ = ('timestamp', 'sensor1', 'sensor2', 'sensor3', 'metadata', 'category')

    def __init__(self):
        # Numeric attributes grouped first
        self.timestamp = 0
        self.sensor1 = 0.0
        self.sensor2 = 0.0
        self.sensor3 = 0.0
        # Non-numeric attributes grouped after
        self.metadata = {}
        self.category = ""
# Better cache usage - accessing related attributes together

# Accessing attributes in scattered order
points = [DataPoint() for _ in range(100000)]

# Poor cache usage - jumping between attributes
for p in points:
    p.sensor1 = random.random()
    p.metadata['key'] = 'value'
    p.sensor2 = random.random()
    p.category = 'A'
    p.sensor3 = random.random()