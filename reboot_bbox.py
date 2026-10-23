import requests
import urllib3

# Désactive les messages d'avertissement SSL de urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
PASSWORD = ""  # Ton mot de passe d'admin Bbox
# ---------------------

def reboot_bbox():
    session = requests.Session()
    session.verify = False  # Ignore la vérification du certificat auto-signé
    
    # 1. Connexion / Authentification
    login_url = "https://mabbox.bytel.fr/api/v1/login"
    print("⏳ Connexion à la Bbox...")
    res_login = session.post(login_url, data={'password': PASSWORD})
    
    if res_login.status_code != 200:
        print(f"❌ Échec de la connexion (Code HTTP: {res_login.status_code})")
        return

    print("🔑 Authentification réussie aller elliot. Récupération du token de sécurité...")
    
    # 2. Récupération du btoken
    token_url = "https://mabbox.bytel.fr/api/v1/device/token"
    res_token = session.get(token_url)
    
    btoken = None
    if res_token.status_code == 200:
        try:
            data = res_token.json()
            # Selon la version du firmware, le token est une chaîne ou un objet JSON
            if isinstance(data, list) and len(data) > 0:
                btoken = data[0].get('device', {}).get('token')
            elif isinstance(data, dict):
                btoken = data.get('device', {}).get('token') or data.get('token') or data.get('btoken')
        except Exception as e:
            print(f"⚠️ Erreur lors de la lecture du JSON : {e}")

    # Si le token n'est pas dans le JSON, on essaie de le lire directement s'il est au format texte
    if not btoken and res_token.text:
        btoken = res_token.text.strip().replace('"', '')

    if not btoken:
        print("❌ Impossible de récupérer le 'btoken'.")
        return

    print(f"⚡ Token obtenu bien joue elliot. Envoi de l'ordre de redémarrage...")

    # 3. Ordre de redémarrage avec le btoken
    reboot_url = f"https://mabbox.bytel.fr/api/v1/device/reboot?btoken={btoken}"
    res_reboot = session.post(reboot_url)
    
    if res_reboot.status_code == 200:
        print("TA REUSSI elliot La Bbox va redémarrer dans quelques secondes.")
    else:
        print(f"❌ Échec tes pas elliot alderson de la commande de redémarrage (Code HTTP: {res_reboot.status_code})")

if __name__ == "__main__":
    reboot_bbox()
