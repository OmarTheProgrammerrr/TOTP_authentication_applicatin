
# Authentication Application

This project is a Flask-based authentication application that supports user registration, login, and Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP). Additionally, it allows users to manage TOTP secret keys and generate TOTP codes.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)

## Project Structure

```
├── Application
│   ├── css
│   │   ├── style.css
│   ├── index.html  ###allows the register, login, generate secret keys and validate TOTPs 
│   ├── js
│   │   ├── index.js
│   │   ├── otp.js
│   │   ├── script.js
│   ├── otp.html
├── Authentication_app
│   ├── css
│   │   ├── style.css
│   ├── index.html    ###allows the user to add secret keys and generate TOTPs
│   ├── js
│   │   ├── app.js
├── Flask_application
│   ├── app.py ## flask application that handles login register and totp generation and validation requests
│   ├── app_debug.py  ## flask in debug mode
│   ├── backend.py ### backend classes to generate, validate TOTPs
│   ├── keys.csv  ### to store users login info (for the server)
│   ├── users.csv ### to store secret keys (for the client)
├── requirements.txt
```

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/OmarTheProgrammerrr/TOTP_authentication_applicatin.git
   cd TOTP_authentication_applicatin
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
   cd Flask_application
   python app.py
   ```

The application should now be running on `http://127.0.0.1:5000`.

## Usage

Run **Application/index.html** to register users and create secret keys for them

Run **Authentication_app/index.html** to add secret keys and using them to generate TOTPs


