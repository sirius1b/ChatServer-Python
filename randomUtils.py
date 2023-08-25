import time

import asyncio

class Subscriber:

    def __init__(self, topic: str, name: str):
        self.topic = topic
        self.name = name
        self.data = []

    def subscribe(self):
        Broker().addSub(self.topic, self)

    def unsubscriber(self):
        Broker().removeSub(self.topic, self)


    async def getUpdate(self):
        while (await len(self.data) > 0):
            continue
        out = self.data
        self.data = []
        return out

    async def update(self, dat) -> None:
        await asyncio.sleep(1)
        # time.sleep(1)
        self.data.append(dat)


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

    async def push(self, topic, data):
        t1 = time.perf_counter()
        print(self.subs, topic, data)
        if (topic in self.subs.keys()):
            sub: Subscriber
            updates = [sub.update(data) for sub in self.subs[topic]]
            await asyncio.gather(*updates)
        print(f'{time.perf_counter() - t1} seconds passed')

class Publisher:
    def __init__(self, topic: str, src: str):
        self.topic = topic
        self.src = src

    async def publish(self, data):
        await Broker().push(self.topic, data)

if __name__ == "__main__":
    for i in range(400):
        s = Subscriber("top", "s" + str(i));
        s.subscribe()
    p = Publisher("top", "src")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(p.publish(1))
    finally:
        loop.close();
