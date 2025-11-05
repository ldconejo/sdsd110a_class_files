from abc import ABC, abstractmethod
from typing import List

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

# Subject (Observable) interface
class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)

# Concrete subject
class WeatherStation(Subject):
    def __init__(self):
        super().__init__()
        self._temperature = 0
        self._humidity = 0
        self._pressure = 0
    
    def set_weather_data(self, temperature, humidity, pressure):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self.notify()  # Notify all observers
    
    @property
    def temperature(self):
        return self._temperature
    
    @property
    def humidity(self):
        return self._humidity
    
    @property
    def pressure(self):
        return self._pressure

# Concrete observers
class CurrentConditionsDisplay(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, subject: WeatherStation):
        print(f"{self.name}: Current conditions - "
              f"Temp: {subject.temperature}°F, "
              f"Humidity: {subject.humidity}%, "
              f"Pressure: {subject.pressure} in")

class ForecastDisplay(Observer):
    def __init__(self):
        self.last_pressure = 0
    
    def update(self, subject: WeatherStation):
        current_pressure = subject.pressure
        if current_pressure > self.last_pressure:
            print("Forecast: Improving weather on the way!")
        elif current_pressure < self.last_pressure:
            print("Forecast: Watch out for cooler, rainy weather")
        else:
            print("Forecast: More of the same")
        self.last_pressure = current_pressure

if __name__ == "__main__":
    # Usage
    weather_station = WeatherStation()

    # Create displays and subscribe to weather station
    current_display = CurrentConditionsDisplay("Phone App")
    forecast_display = ForecastDisplay()

    weather_station.attach(current_display)
    weather_station.attach(forecast_display)

    # Weather changes automatically notify all displays
    weather_station.set_weather_data(80, 65, 30.4)
    weather_station.set_weather_data(82, 70, 29.2)
