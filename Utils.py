
import asyncio

class Subscriber:

    def __init__(self, topic: str):
        self.topic = topic

    def __init__(self, topic: str, name: str):
        self.topic = topic
        self.name = name


    def subscribe(self):
        Broker().addSub(self.topic, self)

    def unsubscribe(self):
        Broker().removeSub(self.topic, self)

    async def update(self, data):
        print(">>>Subcriber: " + self.name)
        print(">>> recevied Data: " + data)
        self.data = data

    async def getUpdate(self) -> dict:
        while (await self.data == None ):
            continue
        return self.data

class Broker:
    __instance = None

    def __new__(cls):

        if (cls.__instance is None):
            cls.__instance = super(Broker, cls).__new__(cls)
            cls.__instance.subs = dict()

        return cls.__instance

    def addSub(self, topic: str,  sub: Subscriber):

        if topic in self.subs.keys():
            self.subs[topic].append(sub)
        else :
            self.subs[topic] = [sub]
        print(self.subs, topic, sub)

    def removeSub(self, topic: str, sub: Subscriber):

        if topic in self.subs.keys():
            if ( sub in self.subs[topic] ):
                self.subs[topic].remove(sub)

    def push(self, topic, data):
        print(self.subs, topic, data)
        if (topic in self.subs.keys()):
            sub: Subscriber
            a
            for sub in self.subs[topic]:
                sub.update(data)

class Publisher:
    def __init__(self, topic: str, src: str):
        self.topic = topic
        self.src = src

    def publish(self, data):
        Broker().push(self.topic, data)

if __name__ == '__main__':
    topic = "abcd"
    p = Publisher(topic)

    s1 = Subscriber(topic, "sub-1")
    s2 = Subscriber(topic, "sub-2")
    s1.subscribe()
    s2.subscribe()

    p.publish("this is data")