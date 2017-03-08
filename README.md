# flask-parsedate

JSON endpoint that parses dates.

### Setup

    pip install flask parsedatetime
    python flask-parsedate.py

### Usage (GET)

    curl http://localhost:5000/?q=<date>


### Usage (POST)

    curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/ -d 'newline delimited series of dates'
