from abc import ABC, abstractmethod
import threading

class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        """Receive update from subject"""
        pass


class Subject:
    def __init__(self):
        self._observers = []
        self._lock = threading.RLock()  # RLock instead of Lock to allow re-entrant locking
    
    def attach(self, observer: Observer):
        with self._lock:
            self._observers.append(observer)
            # Optional: print(f"Attached {observer.__class__.__name__}")

    def detach(self, observer: Observer):
        with self._lock:
            self._observers.remove(observer)
            # Optional: print(f"Detached {observer.__class__.__name__}")

    def notify(self):
        with self._lock:
            observers_copy = list(self._observers)  # Avoid mutation during iteration
        
        for observer in observers_copy:
            observer.update(self)

# Stock price subject
class Stock(Subject):
    def __init__(self, symbol, price):
        super().__init__()
        self.symbol = symbol
        self._price = price
        self._lock = threading.RLock()  # RLock here too for consistency
    
    def set_price(self, price):
        with self._lock:
            old_price = self._price
            self._price = price
            print(f"STOCK: {self.symbol} price changed from ${old_price} to ${price}")
            self.notify()
    
    @property
    def price(self):
        return self._price

# Different types of observers
class PortfolioManager(Observer):
    def __init__(self, name):
        self.name = name
        self.holdings = {}
    
    def add_holding(self, symbol, shares):
        self.holdings[symbol] = shares
    
    def update(self, stock: Stock):
        if stock.symbol in self.holdings:
            shares = self.holdings[stock.symbol]
            value = shares * stock.price
            print(f"PORTFOLIO {self.name}: {stock.symbol} holding worth ${value:,.2f}")

class PriceAlertObserver(Observer):
    def __init__(self, symbol, threshold, alert_type="above"):
        self.symbol = symbol
        self.threshold = threshold
        self.alert_type = alert_type
        self.triggered = False
    
    def update(self, stock: Stock):
        if stock.symbol == self.symbol:
            should_alert = False
            if self.alert_type == "above" and stock.price > self.threshold:
                should_alert = True
            elif self.alert_type == "below" and stock.price < self.threshold:
                should_alert = True
            
            if should_alert and not self.triggered:
                print(f"🚨 ALERT: {stock.symbol} is {self.alert_type} ${self.threshold}! "
                      f"Current price: ${stock.price}")
                self.triggered = True

class TradingBot(Observer):
    def __init__(self, strategy):
        self.strategy = strategy
        self.last_prices = {}
    
    def update(self, stock: Stock):
        last_price = self.last_prices.get(stock.symbol, stock.price)
        
        if stock.price > last_price * 1.05:  # 5% increase
            print(f"🤖 BOT: {stock.symbol} up 5%+ - SELL signal at ${stock.price}")
        elif stock.price < last_price * 0.95:  # 5% decrease
            print(f"🤖 BOT: {stock.symbol} down 5%+ - BUY signal at ${stock.price}")
        
        self.last_prices[stock.symbol] = stock.price

if __name__ == "__main__":
    # Usage
    apple_stock = Stock("AAPL", 150.00)

    # Create different observers
    portfolio = PortfolioManager("Retirement Fund")
    portfolio.add_holding("AAPL", 100)

    high_price_alert = PriceAlertObserver("AAPL", 155, "above")
    low_price_alert = PriceAlertObserver("AAPL", 140, "below")
    trading_bot = TradingBot("momentum")

    # Subscribe observers
    apple_stock.attach(portfolio)
    apple_stock.attach(high_price_alert)
    apple_stock.attach(low_price_alert)
    apple_stock.attach(trading_bot)

    # Price changes notify all observers automatically
    apple_stock.set_price(152.50)  # Portfolio updates
    apple_stock.set_price(158.00)  # High price alert triggers
    apple_stock.set_price(138.75)  # Low price alert triggers, bot signals buy
