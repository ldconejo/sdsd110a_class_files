from abc import ABC, abstractmethod
# Pricing strategies for e-commerce
class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, base_price, customer_info):
        pass

class RegularPricing(PricingStrategy):
    def calculate_price(self, base_price, customer_info):
        return {
            "final_price": base_price,
            "discount": 0,
            "reason": "Regular pricing"
        }

class StudentPricing(PricingStrategy):
    def calculate_price(self, base_price, customer_info):
        discount = base_price * 0.15  # 15% student discount
        return {
            "final_price": base_price - discount,
            "discount": discount,
            "reason": "Student discount (15%)"
        }

class SeniorPricing(PricingStrategy):
    def calculate_price(self, base_price, customer_info):
        discount = base_price * 0.20  # 20% senior discount
        return {
            "final_price": base_price - discount,
            "discount": discount,
            "reason": "Senior discount (20%)"
        }

class VIPPricing(PricingStrategy):
    def calculate_price(self, base_price, customer_info):
        # VIP gets better discount based on loyalty level
        loyalty_years = customer_info.get("loyalty_years", 0)
        discount_rate = min(0.30, 0.10 + (loyalty_years * 0.02))  # Up to 30%
        discount = base_price * discount_rate
        return {
            "final_price": base_price - discount,
            "discount": discount,
            "reason": f"VIP discount ({discount_rate*100:.0f}% - {loyalty_years} years loyalty)"
        }

class BulkPricing(PricingStrategy):
    def calculate_price(self, base_price, customer_info):
        quantity = customer_info.get("quantity", 1)
        if quantity >= 100:
            discount_rate = 0.25  # 25% for 100+
        elif quantity >= 50:
            discount_rate = 0.15  # 15% for 50+
        elif quantity >= 10:
            discount_rate = 0.10  # 10% for 10+
        else:
            discount_rate = 0
        
        discount = base_price * discount_rate
        return {
            "final_price": base_price - discount,
            "discount": discount,
            "reason": f"Bulk discount ({discount_rate*100:.0f}% for {quantity} items)"
        }

# Pricing context
class ProductPricer:
    def __init__(self):
        self.strategy = RegularPricing()
    
    def set_pricing_strategy(self, strategy: PricingStrategy):
        self.strategy = strategy
    
    def get_price(self, base_price, customer_info):
        return self.strategy.calculate_price(base_price, customer_info)

if __name__ == "__main__":
    # Usage - strategy changes based on customer type
    pricer = ProductPricer()
    base_price = 100.00

    # Different customer scenarios
    customers = [
        {"type": "regular", "info": {}},
        {"type": "student", "info": {"student_id": "STU123"}},
        {"type": "senior", "info": {"age": 67}},
        {"type": "vip", "info": {"loyalty_years": 8}},
        {"type": "bulk", "info": {"quantity": 75}}
    ]

    # Strategy factory (could use Factory pattern here too!)
    def get_pricing_strategy(customer_type):
        strategies = {
            "regular": RegularPricing(),
            "student": StudentPricing(),
            "senior": SeniorPricing(),
            "vip": VIPPricing(),
            "bulk": BulkPricing()
        }
        return strategies.get(customer_type, RegularPricing())

    print("=== Pricing Strategy Demonstration ===")
    for customer in customers:
        strategy = get_pricing_strategy(customer["type"])
        pricer.set_pricing_strategy(strategy)
        
        result = pricer.get_price(base_price, customer["info"])
        print(f"\n{customer['type'].upper()} Customer:")
        print(f"  Base price: ${base_price:.2f}")
        print(f"  Final price: ${result['final_price']:.2f}")
        print(f"  Savings: ${result['discount']:.2f}")
        print(f"  Reason: {result['reason']}")
