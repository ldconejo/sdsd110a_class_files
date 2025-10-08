# The problem here is that getting the sum of x values requires
# accessing each Point object, which adds overhead compared to using
# a more efficient data structure like arrays or tuples.
class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

points = [Point(i, i+1, i+2) for i in range(1000000)]
sum_x = sum(p.x for p in points)
