from abc import ABC, abstractmethod

# Component interface
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Concrete component
class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

# Base decorator
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

# Concrete decorators
class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.5
    
    def description(self):
        return self._coffee.description() + ", milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.2
    
    def description(self):
        return self._coffee.description() + ", sugar"

class WhippedCreamDecorator(CoffeeDecorator):
    def cost(self):
        return self._coffee.cost() + 0.7
    
    def description(self):
        return self._coffee.description() + ", whipped cream"

# Usage - can chain decorators
coffee = SimpleCoffee()                    # $2.00, "Simple coffee"
coffee = MilkDecorator(coffee)             # $2.50, "Simple coffee, milk" 
coffee = SugarDecorator(coffee)            # $2.70, "Simple coffee, milk, sugar"
coffee = WhippedCreamDecorator(coffee)     # $3.40, "Simple coffee, milk, sugar, whipped cream"

print(f"{coffee.description()} costs ${coffee.cost()}")
