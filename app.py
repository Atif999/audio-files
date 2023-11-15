from flask import Flask, request, jsonify, g, send_file
from flask_httpauth import HTTPBasicAuth
import sqlite3
import base64
from io import BytesIO

app = Flask(__name__)
auth = HTTPBasicAuth()

# Hard-coded credentials for basic authentication
USERNAME = 'admin'
PASSWORD = 'secret'

# Basic authentication callback function
@auth.verify_password
def verify_password(username, password):
    return username == USERNAME and password == PASSWORD

# Connect to the SQLite database
def connect_db():
    db_file = 'audio_database.db'
    return sqlite3.connect(db_file)

# Create the 'audio' table
def init_db():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio (
            id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            data TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()

# Get the database connection for the current request
def get_db():
    if 'db' not in g:
        g.db = connect_db()
    return g.db

# Close the database connection after each request
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Initialize the database
init_db()

# Endpoint for fetching audio data
@app.route('/audio/<int:audio_id>', methods=['GET'])
@auth.login_required
def get_audio(audio_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, filename, data FROM audio WHERE id = ?', (audio_id,))
    audio = cursor.fetchone()
    if audio:
        if 'file' in request.args and request.args['file'].lower() == 'true':
            audio_bytes = base64.b64decode(audio[2])
            return send_file(BytesIO(audio_bytes), mimetype='audio/wav', as_attachment=True, download_name=audio[1])
        else:
            audio_dict = {'id': audio[0], 'filename': audio[1], 'data': audio[2]}
            return jsonify(audio_dict)
    else:
        return jsonify({'error': 'Audio not found'}), 404

# Endpoint for posting audio data
@app.route('/audio', methods=['POST'])
@auth.login_required
def post_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    audio_data = {
        'filename': file.filename,
        'data': base64.b64encode(file.read()).decode('utf-8')
    }

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO audio (filename, data) VALUES (?, ?)', (audio_data['filename'], audio_data['data']))
    db.commit()

    audio_id = cursor.lastrowid

    return jsonify({'id': audio_id, 'filename': audio_data['filename']}), 201

if __name__ == '__main__':
    app.run(debug=True)
