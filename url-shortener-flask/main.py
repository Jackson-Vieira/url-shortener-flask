import os

from flask import Flask, request, redirect
from pydantic import BaseModel
from unique_id_generator.md5 import MD5Utils
from database import perform_persist_query, perform_query

from dotenv import load_dotenv

from cache import Cache, redis_connect

import json

load_dotenv()

app = Flask(__name__)
cache = Cache(redis_connect())

INSERT_SHORT_URL = """
    INSERT INTO short_url (longURL, shortURL)
    VALUES (%s, %s);
"""

SELECT_SHORT_URL = """
    SELECT longURL FROM short_url
    WHERE shortURL = %s;
"""

COUNT_SHORT_URL = """
    SELECT COUNT(*) FROM short_url;
"""

@app.route('/')
def health_check():
    return "Ok"

class TinyURLIn(BaseModel):
    longURL: str 

class TinyURL(BaseModel):
    id: int
    shortURL: str
    longURL: str

@app.route('/api/v1/data/shorten', methods=['POST'])
def create_short_url():
    try:
        data = TinyURLIn(**request.json)
        short_url = MD5Utils.generate_random_short_url(data.longURL)
        perform_persist_query(INSERT_SHORT_URL, (data.longURL, short_url))
    except Exception as excp:
        print("excp", excp)
        return '', 404
    return {'shortURL': f'http://localhost:5000/api/v1/{short_url}'}

@app.route('/api/v1/data/shorten', methods=['GET'])
def get_short_url():
    count = perform_query(COUNT_SHORT_URL)
    return {'count': count}

@app.route('/api/v1/<short_url>')
def redirect_short_url(short_url: str):

    data = cache.get(short_url)

    if data is not None:
        data = json.loads(data)
        long_url = data.get('longURL')

    else:
        long_url = perform_query(SELECT_SHORT_URL, (short_url,))

        if long_url is None:
            return '', 404

        data = {'longURL': long_url}
        print("Setting cache", short_url, json.dumps(data))
        cache.set(short_url, json.dumps(data))

    print("Redirecting to", long_url)
    return redirect(long_url)

if __name__ == "__main__":
    app.run(debug=True)