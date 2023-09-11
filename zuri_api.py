#!/usr/bin/python3
from flask import Flask, request, jsonify, make_response

import sqlite3

app = Flask(__name__)

app.url_map.strict_slashes = False

# Create SQLite database and table

conn = sqlite3.connect('api.db')

cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS api (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL
        )
        ''')

conn.commit()
conn.close()

# Helper function to validate input

def validate_input(data):
    if 'user_id' not in data:
        return False
    if not isinstance(data['user_id'], str):
        return False
    return True

# CREATE: Addind a new person

@app.route('/api', methods=['POST'])
def create_person():
    data = request.json
    if not validate_input(data):
        return make_response(jsonify({'error': 'Invalid input'}), 400)

    user_id = data['user_id']
    conn = sqlite3.connect('api.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO api (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Person added successfully'}), 201

#READ: Fetching details of a person by name

@app.route('/api/<string:user_id>', methods=['GET'])
def read_person(user_id):
    conn = sqlite3.connect('api.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM api WHERE user_id = ?', (user_id,))
    person = cursor.fetchone()
    conn.close()
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    return jsonify({'user_id': person[1]})

#UPDATE: Modify details of an existing person by name

@app.route('/api/<string:user_id>', methods=['PUT'])
def update_person(user_id):
    data = request.json
    if not validate_input(data):
        return make_response(jsonify({'error': 'Invalid input'}), 400)

    new_name = data['user_id']
    conn = sqlite3.connect('api.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE api SET user_id = ? WHERE user_id = ?', (new_name, user_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Person updated successfully'})

#DELETE: Remove a person by name

@app.route('/api/<string:user_id>', methods=['DELETE'])
def delete_person(user_id):
    conn = sqlite3.connect('api.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM api WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Person deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

