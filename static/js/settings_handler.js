function openSettingsDialog() {
    var overlay = document.getElementById('overlay');
    overlay.style.display = 'flex';
    var dropdown = document.getElementById('platformSelect');
    dropdown.innerHTML = '';
    var option1 = document.createElement('option');
    option1.value = 'steam';
    option1.textContent = 'Steam';
    dropdown.appendChild(option1);
    var option2 = document.createElement('option');
    option2.value = 'epicgames';
    option2.textContent = 'Epic Games';
    dropdown.appendChild(option2);
}

function closeSettingsDialog() {
    var overlay = document.getElementById('overlay');
    overlay.style.display = 'none'; // Hide overlay
}

function handleFileSelection(event) {
    const file = event.target.files[0];
    if (file) {
        console.log("Selected file:", file.name);
        console.log("File path (not accessible due to browser security):", event.target.value);
    }
}