import time

from flask import Flask, json, request, jsonify
import signal
from Utils import Broker, Subscriber
import threading
app = Flask(__name__)

@app.route('/updates', methods=['POST'])
def get():
    body: dict
    body = json.loads(request.get_data())


    if (request.is_json):
        __validate_get_body(body)
        event  = body['event']
        s = Subscriber()
        Broker().register(event, s)
        resp_data = s.getUpdate()

        return jsonify(resp_data),200
    return jsonify({}), 400


@app.route('/publish', methods=['POST'])
def post():

    t1 = time.perf_counter()
    body:dict
    body = json.loads(request.get_data())

    if (request.is_json):
        __validateBody(body)

        topic= body['event'] ; data = body['data']; src = body['src']


        threading.Thread(target=Broker().publish, args=[topic, src, data]).start()
        # with ThreadPoolExecutor() as executor:
        #     executor.submit(Broker().publish(topic, src, data))


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
    exit(0)

if __name__ == '__main__':

    signal.signal(signal.SIGINT, signalHandler)
    Broker().start()
    app.run(debug=True, port=6060)