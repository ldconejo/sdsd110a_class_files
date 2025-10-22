class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

animal_type = input("Enter animal (dog/cat): ")

if animal_type == "dog":
    animal = Dog()
elif animal_type == "cat":
    animal = Cat()

print(animal.speak())
