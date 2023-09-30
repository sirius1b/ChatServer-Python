import time

from flask import Flask, json, request, jsonify
import signal
from Utils import Broker, Subscriber
import threading
app = Flask(__name__)





@app.route('/updates', methods=['POST'])
def get():
    print("updatess=------------------")
    body: dict
    body = json.loads(request.get_data())
    print(request.headers)
    print(body)

    if (request.is_json):
        __validate_get_body(body)
        event  = body['event']
        s = Subscriber()
        Broker().register(event, s)
        resp_data = s.getUpdate()
        print("returning the respone: " + str(resp_data))
        return jsonify(resp_data),200
    return jsonify({}), 400


@app.route('/publish', methods=['POST'])
def post():
    print("publish--------------")
    t1 = time.perf_counter()
    body:dict
    body = json.loads(request.get_data())
    print(body)
    if (request.is_json):
        __validateBody(body)
        print(body)
        topic= body['event'] ; data = body['data']; src = body['src']

        print(f'>>> received request on topic: {topic} from src: {src}, data: {data}')
        print(f'>>> time took {time.perf_counter() - t1}')

        threading.Thread(target=Broker().publish, args=[topic, src, data]).start()
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(Broker().publish(topic, src, data))
        print(f'>>> about to succeed for publish in  {time.perf_counter() - t1}s')

        return jsonify({}), 200
    return jsonify({}), 400


def __validateBody(body: dict):
    if ('event' not in body.keys() or 'data' not in body.keys() or  'src' not in body.keys()):
        raise RuntimeError("Invalid body")

def __validate_get_body(body: dict):
    if ('event' not in body.keys()):
        raise RuntimeError("Invalid body")

def signalHandler(signum, frame):
    Broker().stop()
    print("about to shutdown")
    exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signalHandler)
    Broker().start()
    app.run(debug=True, port=6060)