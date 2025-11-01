import streamlit as st
from pathlib import Path
import json
from hashlib import sha256

st.set_page_config(page_title="Connexion", layout="centered")

# Dossier et fichier utilisateurs
DATA_DIR = Path("donnees")
DATA_DIR.mkdir(exist_ok=True)
FICHIER_UTILISATEURS = DATA_DIR / "utilisateurs.csv"

def charger_utilisateurs():
    if FICHIER_UTILISATEURS.exists():
        with FICHIER_UTILISATEURS.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def hash_mdp(mdp: str) -> str:
    return sha256(mdp.encode("utf-8")).hexdigest()


# CSS pour changer la couleur de fond
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #DBDBDB; }


    }
    </style>
    """,
    unsafe_allow_html=True,
)

# En-tête
st.title("Connexion")
st.write("Connectez-vous et retrouvez votre suivi emploi !")


# Formulaire de connexion
email = st.text_input("Email", key="login_email")
mot_de_passe = st.text_input("Mot de passe", type="password", key="login_mdp")

if st.button("CONNEXION", use_container_width=True, key="btn_connexion"):
    if not email or not mot_de_passe:
        st.warning("Veuillez remplir tous les champs.")
    else:
        users = charger_utilisateurs()
        if email not in users:
            st.error("Aucun compte trouvé avec cet email.")
        elif users[email]["mot_de_passe"] != hash_mdp(mot_de_passe):
            st.error("Mot de passe incorrect.")
        else:
            # Connexion réussie
            st.session_state.user = {
                "email": email,
                "prenom": users[email]["prenom"],
                "nom": users[email]["nom"]
            }
            st.success(f"Content de te revoir {users[email]['prenom']} !")
            st.switch_page("pages/mon_suivi.py")




st.write("---")

# Lien vers la création de compte
st.write("Vous n'avez pas de compte ?")
if st.button("Créer mon compte", use_container_width=True):
        st.switch_page("pages/creation_compte.py")

if st.button("Retour à l'accueil"):
    st.switch_page("accueil.py")