from flask import Flask, json, request, jsonify
from Utils import Publisher, Subscriber
app = Flask(__name__)

@app.route('/publish', methods=['POST'])
def pub():
    body: dict
    body = json.loads(request.get_data())
    if (request.is_json):
        if ('topic' not in body.keys() or 'data' not in body.keys() or  'src' not in body.keys()):
            raise RuntimeError("Invalid body");
        else :
            topic= body['topic'] ; data = body['data']; src = body['src']
            p = Publisher(topic, src)
            p.publish(data) ## <- this should return immediately; this should be async and nonblocking
            return jsonify({}, 200)
    return jsonify({}, 400)

@app.route('/get', methods=['GET'])
def update():
    body: dict
    body = json.loads(request.get_data())
    if (request.is_json):
        if ('topic' not in body.keys() or 'name' not in body.keys()):
            raise RuntimeError("Invalid body");
        else :
            s = Subscriber(topic = body['topic'], name = body['name'])
            data: dict = s.getUpdate()  ## <- this should be blocking a

            return jsonify({}, 200)
    return jsonify({}, 400)

if __name__ == '__main__':
    app.run()