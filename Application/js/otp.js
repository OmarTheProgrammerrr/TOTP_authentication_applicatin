
document.addEventListener("DOMContentLoaded", () => {
    // Get URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const username = urlParams.get('username');  // Get the 'username' query parameter

    if (!username) {
        console.error("Username is missing from the URL query string.");
        alert("Username is missing from the URL. Please log in first.");
        return;  // Stop execution if username is not present
    }

    console.log("Username received from URL:", username);  // Debugging log

    // Set the username in the hidden input field
    document.getElementById('username').value = username;

    // Handle form submission for TOTP verification
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
