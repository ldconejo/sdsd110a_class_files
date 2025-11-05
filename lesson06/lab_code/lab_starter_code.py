from abc import ABC, abstractmethod

# Base component (from slides)
class Coffee(ABC):
    @abstractmethod
    def cost(self):
        pass
    
    @abstractmethod
    def description(self):
        pass

# Concrete component (from slides)
class SimpleCoffee(Coffee):
    def cost(self):
        return 2.0
    
    def description(self):
        return "Simple coffee"

# Base decorator (from slides)
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def cost(self):
        return self._coffee.cost()
    
    def description(self):
        return self._coffee.description()

# Existing decorators (from slides)
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

# TODO: Add your new decorators here!

class VanillaDecorator(CoffeeDecorator):
    def cost(self):
        # TODO: Add $0.60 to the base cost
        pass
    
    def description(self):
        # TODO: Add ", vanilla" to the description
        pass

class ExtraShotDecorator(CoffeeDecorator):
    def cost(self):
        # TODO: Add $0.75 to the base cost
        pass
    
    def description(self):
        # TODO: Add ", extra shot" to the description
        pass
