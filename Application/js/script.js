document.addEventListener("DOMContentLoaded", () => {
    const loginSection = document.getElementById("login-section");
    const registerSection = document.getElementById("register-section");
    const totpSection = document.getElementById("totp-section");
    const toggleToRegister = document.getElementById("toggle-to-register");
    const toggleToLogin = document.getElementById("toggle-to-login");
    const heading = document.querySelector("h1");
    const secretKeyDisplay = document.getElementById("secret-key-display");

    let generatedSecret = ""; // Will store the secret
    let username = ""; // Store the username

    // Toggle between Register and Login sections
    toggleToRegister.addEventListener("click", async () => {
        loginSection.style.display = "none";
        registerSection.style.display = "block";
        heading.textContent = "Register new account";
        document.title = "Register new account";

        // Request a TOTP secret from the server
        const response = await fetch("http://127.0.0.1:5000/generate-secret", {
            method: "GET",
        });

        const result = await response.json();
        if (response.ok) {
            generatedSecret = result.secret; // Store the secret
            secretKeyDisplay.textContent = `Your secret key: ${generatedSecret}`;
        } else {
            alert(result.message);
        }
    });

    toggleToLogin.addEventListener("click", () => {
        registerSection.style.display = "none";
        loginSection.style.display = "block";
        totpSection.style.display = "none";
        heading.textContent = "Login existing account";
        document.title = "Login existing account";
    });

    const registerForm = document.getElementById("register-form");
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(registerForm);
        username = formData.get("username"); // Get the username
        formData.append("secret", generatedSecret); // Add the secret to the form data

        // Hide the first section and show the TOTP input section
        registerSection.style.display = "none";
        totpSection.style.display = "block";
    });

    const totpForm = document.getElementById("totp-form");
    totpForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(totpForm);

        // Append the username and password from the register form
        formData.append("username", username);
        const password = document.getElementById("password").value; // Get the password
        formData.append("password", password);
        formData.append("secret", generatedSecret); // Add the secret to the form data

        // Send registration request with TOTP
        const response = await fetch("http://127.0.0.1:5000/register", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            toggleToLogin.click(); // After successful registration, go to login
        } else {
            alert(result.message);
        }
    });

    const loginForm = document.getElementById("login-form");
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        const formData = new FormData(loginForm);

        const response = await fetch("http://127.0.0.1:5000/login", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        if (response.ok) {
            alert(result.message);
            window.location.href = `otp.html?username=${formData.get("username")}`; // Redirect to otp.html with username
        } else {
            alert(result.message);
        }
    });
});



document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');  // Get the username from the query string

    if (!username) {
        alert("Username is missing from the URL");
        return;  // Stop execution if username is not present
    }

    // Set the username value in the hidden input field
    document.getElementById('username').value = username;

    const totpForm = document.getElementById("totp-form");
    const errorMessage = document.getElementById("error-message");

    totpForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(totpForm);
        const totpCode = formData.get("totp_code");
        const username = formData.get("username");

        try {
            const response = await fetch(`http://127.0.0.1:5000/verify_totp?username=${username}&totp_code=${totpCode}`, {
                method: "POST",
            });

            const result = await response.json();
            if (response.ok) {
                alert(result.message);
                window.location.href = "/success";  // Redirect on success (you can customize this URL)
            } else {
                errorMessage.style.display = "block";
                errorMessage.textContent = result.message;
            }
        } catch (error) {
            errorMessage.style.display = "block";
            errorMessage.textContent = "An error occurred. Please try again.";
        }
    });
});
