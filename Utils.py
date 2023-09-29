

import threading


class Subscriber:

    def __init__(self):
        self.eventData = None

    def updateEvent(self, data: str):
        self.eventData = data

    def getUpdate(self):
        while ( self.eventData == None):
            continue
        return self.eventData


class Broker:
    __instance = None

    def __new__(cls):
        if (cls.__instance is None):
            cls.__instance = super(Broker, cls).__new__(cls)
            cls.__instance.subscriptions = dict()
            cls.__instance.eventQueue = dict()

        return cls.__instance

    def register(self, event: str, subscriber: Subscriber):
        if (event in self.subscriptions.keys()):
            self.subscriptions[event] : list
            self.subscriptions[event].append(subscriber)
        else :
            self.subscriptions[event] = [subscriber]

    def start(self):
        self.status = True
        print("about to in")
        threading.Thread(target=self.run).start()
        print("about to out")

    def stop(self):
        self.status = False

    def run(self):
        while (self.status):

            for event in self.subscriptions.keys():
                if (event in self.eventQueue.keys() and len(self.eventQueue[event]) > 0):
                    for subscriber in self.subscriptions[event]:
                        subscriber: Subscriber
                        subscriber.updateEvent(self.eventQueue[event][0])

                    self.eventQueue[event].pop(0)

    def publish(self, event: str, src: str, data: str):
        print("now put the data")
        if (event in self.eventQueue.keys()):
            self.eventQueue[event] : list
            self.eventQueue[event].append({"src": src, "data": data})
        else :
            self.eventQueue[event] = [{"src": src, "data": data}]
