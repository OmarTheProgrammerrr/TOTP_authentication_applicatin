from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import bcrypt
import os
import logging
import pyotp
from backend import LM_TOTP
import csv

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

DATABASE_FILE = 'users.csv'

if not os.path.exists(DATABASE_FILE):
    pd.DataFrame(columns=['username', 'password_hash', 'totp_secret']).to_csv(DATABASE_FILE, index=False)

def load_users():
    return pd.read_csv(DATABASE_FILE)

def save_users(users_df):
    users_df.to_csv(DATABASE_FILE, index=False)

@app.route('/generate-secret', methods=['GET'])
def generate_secret():
    """Generate a TOTP secret for the user."""
    try:
        totp_secret = pyotp.random_base32()
        logger.info("Generated TOTP secret.")
        return jsonify({'status': 'success', 'secret': totp_secret})
    except Exception as e:
        logger.error(f"Error generating TOTP secret: {e}")
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
            logger.warning(f"Username '{username}' already exists.")
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        # Validate TOTP code
        totp = LM_TOTP(totp_secret)
        if not totp.validate(totp_code):
            logger.warning(f"TOTP validation failed for username '{username}'.")
            return jsonify({'status': 'error', 'message': 'Invalid TOTP code!'}), 400

        # Hash the password and save the user
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = pd.DataFrame({
            'username': [username],
            'password_hash': [hashed_password.decode('utf-8')],
            'totp_secret': [totp_secret]
        })
        users = pd.concat([users, new_user], ignore_index=True)
        save_users(users)

        logger.info(f"User '{username}' registered successfully.")
        return jsonify({'status': 'success', 'message': 'User registered successfully!'})
    
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during registration.'}), 500
    
@app.route('/register', methods=['POST'])
def register():
    try:
        # Debugging: Check what data is being received
        logger.info(f"Request form data: {request.form}")

        # Ensure all necessary fields are provided
        username = request.form.get('username')
        password = request.form.get('password')
        totp_code = request.form.get('totp')
        totp_secret = request.form.get('secret')

        # Check if any of the required fields are missing
        if not all([username, password, totp_code, totp_secret]):
            logger.error("Missing required form data.")
            return jsonify({'status': 'error', 'message': 'Missing required data.'}), 400

        # Load users and check if the username exists
        users = load_users()
        if username in users['username'].values:
            logger.warning(f"Username '{username}' already exists.")
            return jsonify({'status': 'error', 'message': 'Username already exists!'}), 400

        # Validate the TOTP code
        totp = LM_TOTP(totp_secret)  # Assuming you have a TOTP validation class `LM_TOTP`
        if not totp.validate(totp_code):
            logger.warning(f"TOTP validation failed for username '{username}'.")
            return jsonify({'status': 'error', 'message': 'Invalid TOTP code!'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Prepare user data for registration
        new_user = pd.DataFrame({
            'username': [username],
            'password_hash': [hashed_password.decode('utf-8')],
            'totp_secret': [totp_secret]
        })

        # Append new user to the users DataFrame
        users = pd.concat([users, new_user], ignore_index=True)

        # Save the updated user data
        save_users(users)

        logger.info(f"User '{username}' registered successfully.")
        return jsonify({'status': 'success', 'message': 'User registered successfully!'})
    
    except Exception as e:
        logger.error(f"Error during registration: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during registration.'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']

        users = load_users()

        if username not in users['username'].values:
            logger.warning(f"Failed login attempt for non-existent username '{username}'.")
            return jsonify({'status': 'error', 'message': 'Invalid username or password!'}), 400

        user = users[users['username'] == username].iloc[0]
        password_hash = user['password_hash']

        if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
            logger.warning(f"Failed login attempt for username '{username}'. Incorrect password.")
            return jsonify({'status': 'error', 'message': 'Invalid username or password!'}), 400

        logger.info(f"User '{username}' logged in successfully. Proceed to OTP verification.")
        return jsonify({'status': 'success', 'message': 'Login successful! Proceed to OTP verification.'})
    
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return jsonify({'status': 'error', 'message': 'An error occurred during login.'}), 500



@app.route('/verify_totp', methods=['POST'])
def verify_totp():
    
    username = request.args.get('username')
    totp_code = request.args.get('totp_code')
    

    users = load_users()
    user = users[users['username'] == username].iloc[0]
    secret = user['totp_secret']


    totp = LM_TOTP(secret)

    print(totp.now())
    print(totp_code)
    if totp.now() == totp_code:
        logger.info(f"TOTP verification successful for user '{username}'.")
        return jsonify({"status": "success", "message": "TOTP verified successfully!"})
    else:
        logger.warning(f"TOTP verification failed for user '{username}'. Invalid code.")
        return jsonify({"status": "error", "message": "Invalid TOTP code!"}), 400
    

##################################### authentication methods #########################################



DATA_FILE = 'keys.csv'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'secret'])

def read_keys():
    keys = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            keys.append(row)
    return keys


def write_keys(keys):
    with open(DATA_FILE, 'w', newline='') as file:
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
