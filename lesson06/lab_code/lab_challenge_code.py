from barista import *
# Create a coffee with ALL decorators
ultimate_coffee = SimpleCoffee()
ultimate_coffee = MilkDecorator(ultimate_coffee)
ultimate_coffee = SugarDecorator(ultimate_coffee)
ultimate_coffee = VanillaDecorator(ultimate_coffee)
ultimate_coffee = WhippedCreamDecorator(ultimate_coffee)
ultimate_coffee = ExtraShotDecorator(ultimate_coffee)

print("=== Ultimate Coffee ===")
print(f"{ultimate_coffee.description()}")
print(f"Total cost (formatted): ${ultimate_coffee.cost():.2f}")

# What should this cost? Calculate it step by step:
# Simple coffee: $2.00
# + Milk: $0.50 = $2.50
# + Sugar: $0.20 = $2.70
# + Vanilla: $0.60 = $3.30
# + Whipped cream: $0.70 = $4.00
# + Extra shot: $0.75 = $4.75
