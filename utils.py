import secrets
import string
import math

DEFAULT_LENGTH = 8
# Vitesse de crackage estimée (100 milliards d'essais par seconde)
CRACK_SPEED_PER_SECOND = 10**11 
CHAR_USABLE = string.ascii_letters + string.punctuation + string.digits
POOL_SIZE_GEN = len(CHAR_USABLE)

def generate_password(length: int = DEFAULT_LENGTH) -> str:
    """Génère un mot de passe fort aléatoire."""
    # S'assurer que CHAR_USABLE est bien défini
    return ''.join(secrets.choice(CHAR_USABLE) for _ in range(length))

def format_crack_time(seconds):
    """Convertit un nombre de secondes en un format lisible."""
    if seconds < 1: return "Instantané (< 1 seconde)"
    if seconds > 3.154e+19: return "Plusieurs milliards d'années" # Limite pour éviter des chiffres trop grands

    units = [
        (31_536_000 * 100, "siècles"),
        (31_536_000 * 10, "décennies"),
        (31_536_000, "années"),
        (2_592_000, "mois"),
        (604_800, "semaines"),
        (86_400, "jours"),
        (3_600, "heures"),
        (60, "minutes"),
        (1, "secondes")
    ]

    for value, unit in units:
        if seconds >= value:
            return f"{seconds / value:,.1f} {unit}"
            
    return f"{seconds:.2f} secondes"

def analyze_password_strength(password: str) -> dict:
    """Analyse la force, l'entropie, et le temps de crackage estimé du mot de passe."""
    
    # Taille du pool de caractères utilisée pour le calcul d'entropie
    POOL_SIZE = len(string.ascii_letters + string.punctuation + string.digits)
    length = len(password)
    
    if length == 0:
        return {
            "entropy": 0,
            "crack_time_display": "N/A",
            "strength": "Inconnu"
        }

    # Calcul d'entropie (logarithme base 2)
    entropy = length * math.log2(POOL_SIZE)
    
    # Calcul des combinaisons totales (utilisé pour le temps de crackage)
    total_combinations = POOL_SIZE ** length
    
    # Calcul du temps de crackage
    time_seconds = total_combinations / CRACK_SPEED_PER_SECOND

    # Détermination de la force basée sur l'entropie
    if entropy < 40:
        strength = "Weak"
    elif entropy < 60:
        strength = "Medium"
    else:
        strength = "Strong"
        
    time_display = format_crack_time(time_seconds)
        
    return {
        "entropy": round(entropy, 2),
        "crack_time_display": time_display,
        "strength": strength
    }