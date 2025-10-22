class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

class Cow:
    def speak(self):
        return "Moo!"

# Polymorphism in action
def animal_sound(animal):
    print(animal.speak())

# Any class with a speak() method will 
# This is called "duck typing" in Python
# any object that implements the speak method can be used here
animals = [Dog(), Cat(), Cow()]
for a in animals:
    animal_sound(a)
