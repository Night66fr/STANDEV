from flask import Flask, jsonify, request, render_template
# Assurez-vous que l'importation de utils fonctionne correctement
from utils import generate_password, analyze_password_strength 

app = Flask(__name__)

# ====================================================================
# 1. ROUTES DU PORTFOLIO MULTILINGUE
# ====================================================================

# Route Accueil Français (FR) - Nom de fonction: portfolio_home_fr
@app.route('/', methods=['GET']) 
def portfolio_home_fr():
    return render_template('index.html') 

# Route Accueil Anglais (EN) - Nom de fonction: portfolio_home_en
@app.route('/en', methods=['GET'])
def portfolio_home_en():
    return render_template('index-en.html')

# Route Contact Français (FR) - Nom de fonction: contact_fr
@app.route('/contact', methods=['GET']) 
def contact_fr():
    return render_template('contact.html')

# Route Contact Anglais (EN) - Nom de fonction: contact_en
@app.route('/contact-en', methods=['GET'])
def contact_en():
    return render_template('contact-en.html')

# ====================================================================
# 2. ROUTE DE L'OUTIL DE MOT DE PASSE
# Gère l'URL de l'outil (https://standev.vercel.app/pass)
# ====================================================================
@app.route('/pass', methods=['GET']) 
def password_tool(): 
    # Flask cherche et rend templates/pass.html
    return render_template('pass.html') 

# ====================================================================
# 3. API ENDPOINT : GÉNÉRATION DE MOT DE PASSE
# Gère l'appel JS à /api/generate
# ====================================================================
@app.route('/api/generate', methods=['GET'])
def generate_api():
    # Récupère la longueur demandée (défaut à 12)
    length = request.args.get('length', type=int, default=12)
    
    # S'assure d'une longueur minimale
    if length < 8:
        length = 8
        
    # Appelle la fonction de génération
    password = generate_password(length) 
    
    # Retourne le mot de passe en JSON
    return jsonify({'password': password}) 

# ====================================================================
# 4. API ENDPOINT : ANALYSE DE MOT DE PASSE
# Gère l'appel JS à /api/analyze
# ====================================================================
@app.route('/api/analyze', methods=['GET'])
def analyze_api():
    # Récupère le mot de passe à analyser
    pwd = request.args.get('password', type=str)
    
    # Gère le cas où le champ est vide
    if not pwd or pwd.strip() == '':
        return jsonify({
            'strength': 'Inconnu',
            'entropy': 0,
            'crack_time_display': 'N/A'
        })
        
    # Appelle la fonction d'analyse
    results = analyze_password_strength(pwd)
    
    # Retourne les résultats en JSON
    return jsonify(results)

# ====================================================================
# DÉMARRAGE DU SERVEUR
# ====================================================================
if __name__ == '__main__':
    # Lance Flask en mode debug (utile pour les tests locaux)
    app.run(debug=True)

@app.route('/blog_portfolio')
def blog_portfolio():
    return render_template('blog_portfolio.html')

@app.route('/blog_password')
def blog_password_tool():
    return render_template('blog_password.html')