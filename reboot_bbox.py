import requests

# --- CONFIGURATION ---
BBOX_IP = "mabbox.bytel.fr"
PASSWORD = "Brezzo@1313"  # Remplace par ton mot de passe d'admin Bbox
# ---------------------

def reboot_bbox():
    session = requests.Session()
    login_url = f"http://192.168.1.254/api/v1/login"
    
    print("⏳ Connexion à la Bbox...")
    # On envoie l'authentification ('password' est le mot-clé obligatoire pour l'API Bbox)
    res = session.post(login_url, data={'Brezzo@1313': PASSWORD})
    
    if res.status_code == 200:
        data = res.json()
        btoken = data.get('btoken')
        
        if btoken:
            print("🔑 Connexion réussie, envoi de la commande de redémarrage...")
            reboot_url = f"http://192.168.1.254/api/v1/device/reboot?btoken={btoken}"
            reboot_res = session.post(reboot_url)
            
            if reboot_res.status_code == 200:
                print("✅ Ordre envoyé avec succès ! La Bbox va redémarrer dans quelques secondes.")
            else:
                print(f"❌ Échec de la commande de redémarrage (Code HTTP: {reboot_res.status_code})")
        else:
            print("❌ Erreur : Impossible de récupérer le 'btoken' dans la réponse.")
    else:
        print("❌ Erreur de connexion : Mot de passe incorrect ou Bbox inaccessible.")

if __name__ == "__main__":
    reboot_bbox()