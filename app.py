from flask import Flask, jsonify, request, render_template
from utils import generate_password, analyze_password_strength

app = Flask(__name__)

# Route pour la page principale de l'outil
@app.route('/pass.html ', methods=['GET'])
def index():
    return render_template('pass.html') 

# API endpoint pour la génération de mot de passe
@app.route('/api/generate', methods=['GET'])
def generate_api():
    length = request.args.get('length', type=int, default=12)
    
    if length < 4:
        length = 4
        
    password = generate_password(length) 
    
    return jsonify({'password': password}) 

# API endpoint pour l'analyse de mot de passe
@app.route('/api/analyze', methods=['GET'])
def analyze_api():
    pwd = request.args.get('password', type=str)
    
    if not pwd or pwd.strip() == '': # S'assurer que le mot de passe n'est pas vide
        # Retourner une réponse vide mais valide pour le front-end
        return jsonify({
            'strength': 'Inconnu',
            'entropy': 0,
            'crack_time_display': 'N/A'
        })
        
    results = analyze_password_strength(pwd)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)