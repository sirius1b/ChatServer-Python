import time

import asyncio

class Subscriber:

    def __init__(self, topic: str, name: str):
        self.topic = topic
        self.name = name
        self.data = None

    def subscribe(self):
       Broker().addSub(self.topic, self)

    def unsub(self):
        Broker().removeSub(self.topic, self)

    def getUpdate(self):
      while ( self.data == None):
        continue
      out = self.data
      self.data = None
      return out

    async def update(self, data) -> None:
        print(f'----> got update in {self.name} sub, with data: {data}')
        # time.sleep(1)
        self.data = data

    def __repr__(self):
        return f'Subscriber: {self.name}'

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
        print(self.subs)
        t1 = time.perf_counter()
        print(self.subs, topic, data)
        print(f'----> publish in broker, {time.perf_counter() - t1}')
        if (topic in self.subs.keys()):
            sub: Subscriber
            updates = [sub.update(data) for sub in self.subs[topic]]
            print(f'----> publish in broker; update calls, {time.perf_counter() - t1}')
            await asyncio.gather(*updates)
            print(f'----> publish in broker; gather await calls, {time.perf_counter() - t1}')
        print(f'{time.perf_counter() - t1} seconds passed, {time.perf_counter() - t1}')

class Publisher:
    def __init__(self, topic: str, src: str):
        self.topic = topic
        self.src = src

    async def publish(self, data):
        print(f'-----> received a publish request with data: {data}')
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
