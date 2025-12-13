const $generateLength = document.getElementById('generate-length');
const $generatedPassword = document.getElementById('generated-password');
const $testPassword = document.getElementById('test-password');
const $clearTestPasswordBtn = document.getElementById('clear-test-password');
const $strengthOutput = document.getElementById('strength-output');
const $entropyOutput = document.getElementById('entropy-output');
const $timeOutput = document.getElementById('time-output');
const $copyMessage = document.getElementById('copy-message');

document.addEventListener('DOMContentLoaded', () => {
    handleAnalysis(); 
});


function adjustLength(delta) {
    let currentValue = parseInt($generateLength.value);
    const min = parseInt($generateLength.min);
    const max = parseInt($generateLength.max);
    
    let newValue = currentValue + delta;
    
    if (newValue < min) newValue = min;
    if (newValue > max) newValue = max;
    
    $generateLength.value = newValue;
}

function handleGenerate() {
    const length = $generateLength.value;
    
    fetch(`/api/generate?length=${length}`)
        .then(response => response.json())
        .then(data => {
            if (data.password) {
                $generatedPassword.value = data.password;
                analyzePassword(data.password);
            }
        })
        .catch(error => console.error('Erreur lors de la génération:', error));
}


function handleAnalysis() {
    const password = $testPassword.value;

    if (password.length > 0) {
        $clearTestPasswordBtn.classList.add('visible');
    } else {
        $clearTestPasswordBtn.classList.remove('visible');
    }

    analyzePassword(password);
}

function clearTestPassword() {
    $testPassword.value = '';
    handleAnalysis();
    $testPassword.focus();
}

function analyzePassword(password) {
    if (!password || password.trim() === '') {
        $strengthOutput.textContent = '?';
        $strengthOutput.className = 'strength-unknown';
        $entropyOutput.textContent = '? bits';
        $timeOutput.textContent = '?';
        return;
    }
    
    fetch(`/api/analyze?password=${encodeURIComponent(password)}`)
        .then(response => response.json())
        .then(data => {
            $strengthOutput.textContent = data.strength;
            $entropyOutput.textContent = `${data.entropy} bits`;
            $timeOutput.textContent = data.crack_time_display;
            
            $strengthOutput.className = `strength-${data.strength.toLowerCase()}`;
        })
        .catch(error => console.error('Erreur lors de l\'analyse:', error));
}


function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    
    if (element && element.value) {
        navigator.clipboard.writeText(element.value)
            .then(() => {
                $copyMessage.textContent = "Copié dans le presse-papiers !";
                $copyMessage.classList.add('visible');
                
                setTimeout(() => {
                    $copyMessage.classList.remove('visible');
                }, 2500);
            })
            .catch(err => {
                console.error('Erreur de copie:', err);
                $copyMessage.textContent = "Échec de la copie.";
                $copyMessage.classList.add('visible');
                setTimeout(() => {
                    $copyMessage.classList.remove('visible');
                }, 2500);
            });
    }
}