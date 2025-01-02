from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import bcrypt
import os
import pyotp
from backend import LM_TOTP
import csv

app = Flask(__name__)
CORS(app)

USERS_DATA = 'users.csv'

if not os.path.exists(USERS_DATA):
    pd.DataFrame(columns=['username', 'password_hash', 'totp_secret']).to_csv(USERS_DATA, index=False)

def load_users():
    return pd.read_csv(USERS_DATA)

def save_users(users_df):
    users_df.to_csv(USERS_DATA, index=False)

@app.route('/generate-secret', methods=['GET'])
def generate_secret():
    try:
        totp_secret = pyotp.random_base32()
        return jsonify({'status': 'success', 'secret': totp_secret})
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Could not generate TOTP secret.'}), 500

@app.route('/register_', methods=['POST'])
def register_():
    try:
        username = request.form['username']
        password = request.form['password']
        totp_code = request.form['totp']
        totp_secret = request.form['secret']

        users = load_users()

        if username in users['username'].values:
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        totp = LM_TOTP(totp_secret)
        if not totp.validate(totp_code):
            return jsonify({'status': 'error', 'message': 'Invalid TOTP code!'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = pd.DataFrame({
            'username': [username],
            'password_hash': [hashed_password.decode('utf-8')],
            'totp_secret': [totp_secret]
        })
        users = pd.concat([users, new_user], ignore_index=True)
        save_users(users)

        return jsonify({'status': 'success', 'message': 'User registered successfully!'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred during registration.'}), 500
    
@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        totp_code = request.form.get('totp')
        totp_secret = request.form.get('secret')

        if not all([username, password, totp_code, totp_secret]):
            return jsonify({'status': 'error', 'message': 'Missing required data.'}), 400

        users = load_users()
        if username in users['username'].values:
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        totp = LM_TOTP(totp_secret)
        if not totp.validate(totp_code):
            return jsonify({'status': 'error', 'message': 'Invalid TOTP code!'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        new_user = pd.DataFrame({
            'username': [username],
            'password_hash': [hashed_password.decode('utf-8')],
            'totp_secret': [totp_secret]
        })

        users = pd.concat([users, new_user], ignore_index=True)

        save_users(users)

        return jsonify({'status': 'success', 'message': 'User registered successfully!'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred during registration.'}), 500



@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username not in users['username'].values:
            return jsonify({'status': 'error', 'message': 'Invalid username or password!'}), 400

        user = users[users['username'] == username].iloc[0]
        password_hash = user['password_hash']

        if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            return jsonify({'status': 'error', 'message': 'Invalid username or password!'}), 400

        return jsonify({'status': 'success', 'message': 'Login successful! Proceed to OTP verification.'})
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'An error occurred during login.'}), 500


@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    username = request.args.get('username')
    totp_code = request.args.get('totp_code')

    users = load_users()
    user = users[users['username'] == username].iloc[0]
    secret = user['totp_secret']

    totp = LM_TOTP(secret)

    if totp.now() == totp_code:
        return jsonify({"status": "success", "message": "TOTP verified successfully!"})
    else:
        return jsonify({"status": "error", "message": "Invalid TOTP code!"}), 400


##################################### authentication methods #########################################




KEYS_FILE = 'keys.csv'


if not os.path.exists(KEYS_FILE):
    with open(KEYS_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'secret'])


def read_keys():
    keys = []
    with open(KEYS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keys.append(row)
    return keys



def write_keys(keys):
    with open(KEYS_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'secret'])
        writer.writeheader()
        writer.writerows(keys)




@app.route('/keys', methods=['GET'])
def get_keys():
    keys = read_keys()
    return jsonify(keys)




@app.route('/add-key', methods=['POST'])
def add_key():
    data = request.get_json()
    keys = read_keys()
    keys.append({'name': data['name'], 'secret': data['secret']})
    write_keys(keys)
    return jsonify({'message': 'Key added successfully'}), 201




@app.route('/delete-key/<int:index>', methods=['DELETE'])
def delete_key(index):
    keys = read_keys()
    if 0 <= index < len(keys):
        keys.pop(index)
        write_keys(keys)
        return jsonify({'message': 'Key deleted successfully'}), 200
    return jsonify({'error': 'Invalid key index'}), 400




@app.route('/generate-totp/<int:index>', methods=['GET'])
def generate_totp(index):
    keys = read_keys()
    if 0 <= index < len(keys):
        key = keys[index]
        secret = key['secret']

        totp = LM_TOTP(secret)

        return jsonify({'name': key['name'], 'totp': totp.now()}), 200
    
    return jsonify({'error': 'Invalid key index'}), 400




################ run flask server ################################

if __name__ == '__main__':
    app.run(debug=True)
