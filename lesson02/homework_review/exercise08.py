import random

class DataPoint:
    def __init__(self):
        self.timestamp = 0
        self.sensor1 = 0.0
        self.metadata = {}
        self.sensor2 = 0.0
        self.category = ""
        self.sensor3 = 0.0

# Accessing attributes in scattered order
points = [DataPoint() for _ in range(100000)]

# Poor cache usage - jumping between attributes
for p in points:
    p.sensor1 = random.random()
    p.metadata['key'] = 'value'
    p.sensor2 = random.random()
    p.category = 'A'
    p.sensor3 = random.random()
