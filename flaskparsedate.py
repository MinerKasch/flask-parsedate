import json
import time
import dateparser
from flask import Flask, Response, request
import parsedatetime as pdt
app = Flask(__name__)
p = pdt.Calendar()


HOST='0.0.0.0'
PORT=5000
TIME_FORMAT = '%Y-%m-%d'


def parse1(query):
    parsed = p.parse(query)[0]
    date = time.strftime(TIME_FORMAT, parsed)

    return date


def parse2(query):
    parsed = dateparser.parse(query)
    try:
        date = parsed.strftime(TIME_FORMAT)
    except AttributeError:
        return None

    return date


@app.route('/', methods = ['GET', 'POST'])
def api_root():
    if request.method == 'GET':
        date1 = parse1(request.args['q'])
        date2 = parse2(request.args['q'])

        if (date2 is None or date1 != date2):
            output = 'Error matching parsed dates'
        else:
            output = date1

        js = json.dumps({
                'input': request.args['q'],
                'output': output
        })

    elif request.method == 'POST':
        dates1 = [parse1(line) for line in request.js.split('\n')]
        dates2 = [parse2(line) for line in request.js.split('\n')]
        output = []

        for i in range(len(dates1)):
            if dates2[i] is None or dates1[i] != dates2[i]:
                output.append('Error matching parsed dates')
            else:
                output.append(dates1[i])

        js = json.dumps({
                'input': request.js,
                'output': output
        })

    resp = Response(js, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
