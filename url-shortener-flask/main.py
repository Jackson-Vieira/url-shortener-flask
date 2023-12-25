from flask import Flask, request, redirect
from pydantic import BaseModel

# cache for redirect urls (HASH) key value
# postgres database for persist clicks and other data

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Ok"

class ShortURLCreate(BaseModel):
    longURL: str 

@app.route('/api/v1/data/shorten', methods=['POST'])
def create_short_url():
    try:
        data = ShortURLCreate(**request.get_json())
        print(data)
    except Exception as excp:
        return '', 404
    return '', 202

@app.route('/api/v1/<short_url>')
def redirect_short_url(short_url: str):
    print(short_url)
    return redirect(location="https://amazon.com.br", code=302)

if __name__ == "__main__":
    app.run(debug=True)