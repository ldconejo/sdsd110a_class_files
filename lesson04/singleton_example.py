class Singleton:
    _instance = None  # Class-level attribute

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Example use
s1 = Singleton()
s2 = Singleton()

print(s1 is s2)  # True — both are the same instance
