import requests
import urllib3

# Masque les avertissements de certificat SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
PASSWORD = "Brezzo@1313"  # Ton mot de passe d'admin Bbox
# ---------------------

def reboot_bbox():
    session = requests.Session()
    session.verify = False  # Ignore la vérification du certificat auto-signé
    
    login_url = "https://mabbox.bytel.fr/api/v1/login"
    
    print("⏳ Connexion à la Bbox...")
    res = session.post(login_url, data={'password': PASSWORD})
    
    if res.status_code == 200:
        print("🔑 Connexion réussie ! Envoi de l'ordre de redémarrage...")
        
        # Envoi de la commande de reboot en réutilisant la même session (avec le cookie BBOX_ID)
        reboot_url = "https://mabbox.bytel.fr/api/v1/device/reboot"
        reboot_res = session.post(reboot_url)
        
        if reboot_res.status_code == 200:
            print("✅ Ordre envoyé avec succès ! La Bbox est en cours de redémarrage.")
        else:
            print(f"❌ Échec de la commande de redémarrage (Code HTTP: {reboot_res.status_code})")
    else:
        print(f"❌ Erreur de connexion (Code HTTP: {res.status_code})")

if __name__ == "__main__":
    reboot_bbox()
