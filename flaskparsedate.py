import json
import time
import dateparser
import dateutil.parser
from flask import Flask, Response, request
import parsedatetime as pdt
app = Flask(__name__)
p = pdt.Calendar()


HOST='0.0.0.0'
PORT=5000
TIME_FORMAT = '%Y-%m-%d'


def parse(query):
    date1 = parse1(query)
    date2 = parse2(query)
    date3 = parse3(query)

    # 3 matches (perfect)
    if (date1 is not None and date2 is not None and date3 is not None \
            and date1 == date2 and date2 == date3):
        output = date1
        error = ''

    # 2 matches (good enough)
    elif (date1 is not None and date2 is not None \
            and date1 == date2 and date1 != date3):
        output = date1
        error = 'dateutil failed: ' + str(date3)
    elif (date1 is not None and date3 is not None \
            and date1 == date3 and date1 != date2):
        output = date1
        error = 'dateparser failed: ' + str(date2)
    elif (date2 is not None and date3 is not None \
            and date2 == date3 and date1 != date2):
        output = date2
        error = 'parsedatetime failed: ' + str(date1)

    # no matches (nope)
    else:
        output = ''
        error = 'parsedatetime: {0}; dateparser: {1}; dateutil: {2}'.format(date1, date2, date3)

    js = json.dumps({
        'input': query,
        'output': output,
        'error': error
    })

    return js


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


def parse3(query):
    try:
        parsed = dateutil.parser.parse(query)
    except ValueError:
        return None
    date = parsed.strftime(TIME_FORMAT)

    return date


@app.route('/', methods = ['GET', 'POST'])
def api_root():
    if request.method == 'GET':
        js = parse(request.args['q'])

    elif request.method == 'POST':
        js = [parse(line) for line in request.js.split('\n')]

    resp = Response(js, status=200, mimetype='application/json')

    return resp


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
