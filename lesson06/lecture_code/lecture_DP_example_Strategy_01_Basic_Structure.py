from abc import ABC, abstractmethod

# Strategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Concrete strategies
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number, cvv):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount):
        print(f"Paid ${amount} using Credit Card ending in {self.card_number[-4:]}")
        return {"status": "success", "transaction_id": "CC123456"}

class PayPalPayment(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        print(f"Paid ${amount} using PayPal account {self.email}")
        return {"status": "success", "transaction_id": "PP789012"}

class BankTransferPayment(PaymentStrategy):
    def __init__(self, account_number, routing_number):
        self.account_number = account_number
        self.routing_number = routing_number
    
    def pay(self, amount):
        print(f"Paid ${amount} using Bank Transfer from account {self.account_number}")
        return {"status": "success", "transaction_id": "BT345678"}

# Context class
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(item["price"] for item in self.items)
        print(f"\nCheckout Summary:")
        for item in self.items:
            print(f"  {item['item']}: ${item['price']}")
        print(f"Total: ${total}")
        
        if self.payment_strategy:
            result = self.payment_strategy.pay(total)
            print(f"Payment result: {result}")
            return result
        else:
            print("No payment method selected!")
            return {"status": "failed", "error": "No payment method"}

if __name__ == "__main__":
    # Usage - can change strategy at runtime
    cart = ShoppingCart()
    cart.add_item("Laptop", 999.99)
    cart.add_item("Mouse", 29.99)

    # Customer chooses credit card
    credit_card = CreditCardPayment("1234567812345678", "123")
    cart.set_payment_strategy(credit_card)
    cart.checkout()

    # Later, customer switches to PayPal
    paypal = PayPalPayment("customer@email.com")
    cart.set_payment_strategy(None)
    cart.checkout()
