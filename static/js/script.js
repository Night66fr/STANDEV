document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle');
    const body = document.body;
    
    // Le thème sombre est par défaut dans le CSS, on ne fait rien
    // On vérifie si un thème a été enregistré localement
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        body.classList.add('light-theme');
        toggleButton.textContent = '☀️'; // Change l'icône si le thème clair est chargé
    }

    toggleButton.addEventListener('click', () => {
        body.classList.toggle('light-theme');

        // Met à jour le texte du bouton et enregistre la préférence
        if (body.classList.contains('light-theme')) {
            toggleButton.textContent = '☀️';
            localStorage.setItem('theme', 'light');
        } else {
            toggleButton.textContent = '🌙';
            localStorage.setItem('theme', 'dark');
        }
    });
});