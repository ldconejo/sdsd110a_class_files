class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)


class Observer:
    def update(self, message):
        raise NotImplementedError


class EmailSubscriber(Observer):
    def update(self, message):
        print(f"Email received: {message}")


class SMSSubscriber(Observer):
    def update(self, message):
        print(f"SMS received: {message}")


# Usage
news_channel = Subject()
email_user = EmailSubscriber()
sms_user = SMSSubscriber()

news_channel.attach(email_user)
news_channel.attach(sms_user)

news_channel.notify("New video posted!")  
