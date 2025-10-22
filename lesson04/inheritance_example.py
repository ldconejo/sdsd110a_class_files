class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some generic sound"

# Subclass inherits from Animal
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # call parent constructor
        self.breed = breed
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
    
if __name__ == "__main__":
    dog = Dog("Buddy", "Golden Retriever")
    cat = Cat("Whiskers")
    
    print(f"{dog.name} says: {dog.speak()}")
    print(f"{dog.name} is a {dog.breed}")
    print(f"{cat.name} says: {cat.speak()}")