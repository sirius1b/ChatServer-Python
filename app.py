import time

from flask import Flask, json, request, jsonify, Response
from randomUtils import Publisher, Subscriber
import asyncio
app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def pub():
    t1 = time.perf_counter()
    body: dict
    body = json.loads(request.get_data())
    if (request.is_json):
        if ('topic' not in body.keys() or 'data' not in body.keys() or  'src' not in body.keys()):
            raise RuntimeError("Invalid body");
        else :
            topic= body['topic'] ; data = body['data']; src = body['src']
            print(f'>>> received request on topic: {topic} from src: {src}, data: {data}')
            print(f'>>> time took {time.perf_counter() - t1}')

            loop = asyncio.new_event_loop()
            print(f'>>> time took {time.perf_counter() - t1}, created event loop')

            asyncio.set_event_loop(loop)
            print(f'>>> time took {time.perf_counter() - t1}, set event loop')
            try:
                p = Publisher(topic, src)
                print(f'>>> time took {time.perf_counter() - t1}, instantiated event loop')
                loop.run_until_complete(p.publish(data)) ## <- this should return immediately; this should be async and nonblocking
                print(f'>>> time took {time.perf_counter() - t1}, ran the publish')
            finally:
                loop.close()
                print(f'>>> time took {time.perf_counter() - t1}, closed the loop')
            return jsonify({}, 200)
    return jsonify({}, 400)


def format(msg):
    return f'data: {msg} \n\n'

@app.route('/get', methods=['POST', 'GET'])
def update():
    body: dict
    body = json.loads(request.get_data())

    if (request.is_json):
        if ('topic' not in body.keys() or 'name' not in body.keys()):
            raise RuntimeError("Invalid body");
        else :
            def stream() :
                s = Subscriber(topic=body['topic'], name=body['name'])
                try:
                    s.subscribe()
                    t1 = time.perf_counter()
                    while True:
                        data = s.getUpdate()
                        value = data + f' |time-> {time.perf_counter() - t1} s'
                        t1 = time.perf_counter()
                        yield format(value)
                finally:
                    s.unsub()
                    del s
            return Response(stream(), mimetype="text/event-stream")

    return jsonify({}, 400)

if __name__ == '__main__':
    app.run(port=6060)