
# Authentication Application

This project is a Flask-based authentication application that supports user registration, login, and Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP). Additionally, it allows users to manage TOTP secret keys and generate TOTP codes.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [License](#license)

## Project Structure

```
authentication_application/
│
├── app.py                    # Main application file
├── users.csv                 # Stores registered users
├── keys.csv                  # Stores TOTP keys
├── templates/
│   ├── index.html            # Main page for signing in and validating TOTPs
│   └── authenticate.html     # Page for adding secret keys and generating TOTPs
├── static/
│   └── styles.css            # (Optional) Stylesheet for your HTML templates
├── backend.py                # Backend logic for handling TOTP (LM_TOTP class)
└── README.md                 # This README file
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/authentication_application.git
   cd authentication_application
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

The application should now be running on `http://127.0.0.1:5000`.

## Usage

### Registration and Login

1. **Register a new user:**
   - Send a POST request to `/register` with `username`, `password`, `totp`, and `secret`.

2. **Login:**
   - Send a POST request to `/login` with `username` and `password`.

3. **Verify TOTP:**
   - Send a POST request to `/verify_totp` with `username` and `totp_code`.

### Managing TOTP Keys

1. **Get all keys:**
   - Send a GET request to `/keys`.

2. **Add a new key:**
   - Send a POST request to `/add-key` with `name` and `secret`.

3. **Delete a key:**
   - Send a DELETE request to `/delete-key/<index>` with the index of the key to be deleted.

4. **Generate TOTP code:**
   - Send a GET request to `/generate-totp/<index>` with the index of the key.

## Endpoints

### User Management

- **`GET /generate-secret`**
  - Generates a new TOTP secret.

- **`POST /register`**
  - Registers a new user with `username`, `password`, `totp`, and `secret`.

- **`POST /login`**
  - Logs in a user with `username` and `password`.

- **`POST /verify_totp`**
  - Verifies a TOTP code with `username` and `totp_code`.

### Key Management

- **`GET /keys`**
  - Retrieves all stored TOTP keys.

- **`POST /add-key`**
  - Adds a new TOTP key with `name` and `secret`.

- **`DELETE /delete-key/<index>`**
  - Deletes a TOTP key at the specified index.

- **`GET /generate-totp/<index>`**
  - Generates a TOTP code for the key at the specified index.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
