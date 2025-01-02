document.addEventListener('DOMContentLoaded', () => {
    const addKeyForm = document.getElementById('add-key-form');
    const keysList = document.getElementById('keys-list');

    const renderKeys = (keys) => {
        keysList.innerHTML = '';
        keys.forEach((key, index) => {
            const li = document.createElement('li');
            li.innerHTML = `${key.name} 
                <button class="btn-generate" data-index="${index}">Generate TOTP</button> 
                <button class="btn-delete" data-index="${index}">Delete</button>`;
            keysList.appendChild(li);
        });
    };

    const fetchKeys = async () => {
        const response = await fetch('http://127.0.0.1:5000/keys');
        const data = await response.json();
        renderKeys(data);
    };

    const addKey = async (keyName, secretKey) => {
        await fetch('http://127.0.0.1:5000/add-key', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: keyName, secret: secretKey }),
        });
        fetchKeys();
    };

    const deleteKey = async (index) => {
        await fetch(`http://127.0.0.1:5000/delete-key/${index}`, {
            method: 'DELETE',
        });
        fetchKeys();
    };

    const generateTOTP = async (index) => {
        const response = await fetch(`http://127.0.0.1:5000/generate-totp/${index}`);
        const data = await response.json();
        alert(`TOTP for ${data.name}: ${data.totp}`);
    };

    addKeyForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const keyName = document.getElementById('key-name').value;
        const secretKey = document.getElementById('secret-key').value;
        addKey(keyName, secretKey);
        addKeyForm.reset();
    });

    keysList.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-delete')) {
            const index = e.target.getAttribute('data-index');
            deleteKey(index);
        } else if (e.target.classList.contains('btn-generate')) {
            const index = e.target.getAttribute('data-index');
            generateTOTP(index);
        }
    });

    fetchKeys();
});
