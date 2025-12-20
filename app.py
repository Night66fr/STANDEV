from flask import Flask, jsonify, request, render_template
# Importation des fonctions depuis utils.py
from utils import generate_password, analyze_password_strength 

app = Flask(__name__)

# ====================================================================
# 1. ROUTES DU PORTFOLIO (FRANÇAIS)
# ====================================================================

@app.route('/', methods=['GET']) 
def portfolio_home_fr():
    return render_template('index.html') 

@app.route('/contact', methods=['GET']) 
def contact_fr():
    return render_template('contact.html')

@app.route('/pass', methods=['GET']) 
def password_tool(): 
    return render_template('pass.html') 

@app.route('/blog_portfolio')
def blog_portfolio():
    return render_template('blog_portfolio.html')

@app.route('/blog_password')
def blog_password_tool():
    return render_template('blog_password.html')


# ====================================================================
# 2. ROUTES DU PORTFOLIO (ANGLAIS)
# ====================================================================

@app.route('/en', methods=['GET'])
def portfolio_home_en():
    return render_template('index-en.html')

@app.route('/contact-en', methods=['GET'])
def contact_en():
    return render_template('contact-en.html')

@app.route('/en/password-tool')
def password_tool_en():
    return render_template('pass-en.html')

@app.route('/en/blog/portfolio-build')
def blog_portfolio_en():
    return render_template('blog_portfolio_en.html')

@app.route('/en/blog/password-security')
def blog_password_tool_en():
    return render_template('blog_password_en.html')


# ====================================================================
# 3. API ENDPOINTS (LOGIQUE COMMUNE)
# ====================================================================

@app.route('/api/generate', methods=['GET'])
def generate_api():
    length = request.args.get('length', type=int, default=12)
    if length < 8: length = 8
    
    password = generate_password(length) 
    return jsonify({'password': password}) 

@app.route('/api/analyze', methods=['GET'])
def analyze_api():
    pwd = request.args.get('password', type=str)
    
    if not pwd or pwd.strip() == '':
        return jsonify({
            'strength': 'Inconnu',
            'entropy': 0,
            'crack_time_display': 'N/A'
        })
        
    # Utilise ta version optimisée de utils.py (calcul dynamique du pool)
    results = analyze_password_strength(pwd)
    return jsonify(results)


# ====================================================================
# DÉMARRAGE
# ====================================================================
if __name__ == '__main__':
    app.run(debug=True)