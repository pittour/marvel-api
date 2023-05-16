import hashlib
import time
from flask import Flask, jsonify, redirect, render_template
import requests
from flask_bootstrap import Bootstrap
from models.character import Character

app = Flask(__name__)
app.config.from_pyfile('config.py')
Bootstrap(app)

PUBLIC_KEY = app.config['MARVEL_PUBLIC_KEY']
PRIVATE_KEY =  app.config['MARVEL_PRIVATE_KEY']
BASE_URL = 'http://gateway.marvel.com/v1/public/'

def generate_hash(ts, private_key, public_key):
    m = hashlib.md5()
    m.update(f"{ts}{private_key}{public_key}".encode('utf-8'))
    return m.hexdigest()

@app.route('/characters')
def get_characters():
    ts = str(time.time())
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash,
        'limit': 100
    }
    response = requests.get(f"{BASE_URL}characters", params=params)
    return jsonify(response.json())

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash']
    }
    reponse = requests.get(f"{BASE_URL}characters/{character_id}", params=params)
    return jsonify(reponse.json())

def generate_ts_hash():
    ts = str(time.time())
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)
    return {'ts': ts, 'hash': hash}

@app.route('/boot_character/<int:character_id>', methods=['GET'])
def boot_character(character_id):
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash']
    }
    response = requests.get(f"{BASE_URL}characters/{character_id}", params=params)
    character_data = response.json()["data"]["results"][0]
    boot_character = Character.from_dict(character_data)
    return render_template('character.html', character=boot_character)

@app.route('/comics', methods=['GET'])
def comics():
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash'],
        'limit' : 100
    }
    response = requests.get(f"{BASE_URL}comics", params=params)
    return jsonify(response.json())

@app.route('/series', methods=['GET'])
def series():
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash'],
        'limit' : 100
    }
    response = requests.get(f"{BASE_URL}series", params=params)
    return jsonify(response.json())

@app.route('/stories', methods=['GET'])
def stories():
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash'],
        'limit' : 100
    }
    response = requests.get(f"{BASE_URL}events", params=params)
    return jsonify(response.json())

@app.route('/events', methods=['GET'])
def events():
    ts_hash = generate_ts_hash()
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash'],
        'limit' : 100
    }
    response = requests.get(f"{BASE_URL}events", params=params)
    return jsonify(response.json())

@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"404 - Page Non Trouvée {e}")
    return "500 - Erreur serveur", 500

@app.errorhandler(404)
def server_error(e):
    return redirect('/characters')

app.run(debug=False)