document.getElementById('generateBtn').addEventListener('click', function() {
    const length = document.getElementById('length').value;
    const includeSpecialChars = document.getElementById('specialChars').checked;

    const password = generatePassword(length, includeSpecialChars);
    document.getElementById('password').value = password;
});

document.getElementById('copyBtn').addEventListener('click', function() {
    const passwordField = document.getElementById('password');
    passwordField.select();
    document.execCommand('copy');
    alert('Пароль скопирован в буфер обмена');
});

function generatePassword(length, includeSpecialChars) {
    const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const specialChars = "!@#$%^&*()_-+=<>?/{}[]|";
    let characters = charset;

    if (includeSpecialChars) {
        characters += specialChars;
    }

    let password = "";
    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * characters.length);
        password += characters[randomIndex];
    }

    return password;
}
