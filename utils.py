import secrets
import string
import math

DEFAULT_LENGTH = 12
# Vitesse de crackage : 100 milliards (10^11) de tests/seconde (standard d'un cluster GPU)
CRACK_SPEED_PER_SECOND = 10**11 

def generate_password(length: int = DEFAULT_LENGTH) -> str:
    """Génère un mot de passe réellement aléatoire sur tout le pool disponible."""
    chars = string.ascii_letters + string.punctuation + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

def format_crack_time(seconds):
    """Convertit les secondes en format humainement lisible."""
    if seconds < 1: return "Instantané"
    
    units = [
        (31_536_000 * 100, "siècles"),
        (31_536_000, "ans"),
        (2_592_000, "mois"),
        (86_400, "jours"),
        (3_600, "heures"),
        (60, "minutes"),
        (1, "secondes")
    ]

    for value, unit in units:
        if seconds >= value:
            res = seconds / value
            return f"{res:,.1f} {unit}"
    return f"{seconds:.1f} secondes"

def analyze_password_strength(password: str) -> dict:
    """Analyse la force basée sur les jeux de caractères RÉELLEMENT présents."""
    length = len(password)
    if length == 0:
        return {"entropy": 0, "crack_time_display": "N/A", "strength": "Inconnu"}

    # 1. Calculer la taille du pool RÉEL (R)
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password): pool_size += 26
    if any(c in string.ascii_uppercase for c in password): pool_size += 26
    if any(c in string.digits for c in password): pool_size += 10
    if any(c in string.punctuation for c in password) or any(c == ' ' for c in password): 
        pool_size += 32

    # Sécurité au cas où un caractère exotique est utilisé
    if pool_size == 0: pool_size = 10 

    # 2. Calcul de l'entropie : E = L * log2(R)
    entropy = length * math.log2(pool_size)
    
    # 3. Calcul du temps de crackage (Nombre de combinaisons / Vitesse)
    # Combinaisons = R^L
    total_combinations = pool_size ** length
    time_seconds = total_combinations / CRACK_SPEED_PER_SECOND

    # 4. Détermination de la force (Standards de l'ANSSI)
    if entropy < 64:
        strength = "Faible"
    elif entropy < 80:
        strength = "Moyen"
    elif entropy < 100:
        strength = "Fort"
    else:
        strength = "Très Fort"
        
    return {
        "entropy": round(entropy, 2),
        "crack_time_display": format_crack_time(time_seconds),
        "strength": strength
    }