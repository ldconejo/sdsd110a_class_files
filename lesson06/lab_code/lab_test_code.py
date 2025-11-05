from barista import *
# Test your new decorators
print("=== Testing New Decorators ===")

# Test 1: Simple coffee with vanilla
coffee1 = SimpleCoffee()
coffee1 = VanillaDecorator(coffee1)
print(f"Test 1: {coffee1.description()} costs ${coffee1.cost()}")
# Expected: "Simple coffee, vanilla costs $2.60"

# Test 2: Simple coffee with extra shot
coffee2 = SimpleCoffee()
coffee2 = ExtraShotDecorator(coffee2)
print(f"Test 2: {coffee2.description()} costs ${coffee2.cost()}")
# Expected: "Simple coffee, extra shot costs $2.75"

# Test 3: Combine your new decorators
coffee3 = SimpleCoffee()
coffee3 = VanillaDecorator(coffee3)
coffee3 = ExtraShotDecorator(coffee3)
print(f"Test 3: {coffee3.description()} costs ${coffee3.cost()}")
# Expected: "Simple coffee, vanilla, extra shot costs $3.35"
