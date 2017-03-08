import json
import time
from flask import Flask, Response, request
import parsedatetime as pdt
app = Flask(__name__)
p = pdt.Calendar()


HOST='0.0.0.0'
PORT=5000
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def parse(query):
    parsed = p.parse(query)[0]
    date = time.strftime(TIME_FORMAT, parsed)

    return date


@app.route('/', methods = ['GET', 'POST'])
def api_root():
    if request.method == 'GET':
        date = parse(request.args['q'])
        js = json.dumps({
                'input': request.args['q'],
                'output': date
        })

    elif request.method == 'POST':
        dates = [parse(line) for line in request.js.split('\n')]
        js = json.dumps({
                'input': request.js,
                'output': '\n'.join(dates)
        })

    resp = Response(js, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
