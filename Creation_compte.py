import streamlit as st 
import pandas as pd
import json
from pathlib import Path
from hashlib import sha256

st.set_page_config(page_title="Créer votre compte", layout="centered")

# CSS pour changer la couleur de fond
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #DBDBDB; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Fichier utilisateurs
DATA_DIR = Path("donnees")
DATA_DIR.mkdir(exist_ok=True)
FICHIER_UTILISATEURS = DATA_DIR / "utilisateurs.csv"

def charger_utilisateurs():
    if FICHIER_UTILISATEURS.exists():
        with FICHIER_UTILISATEURS.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def sauvegarder_utilisateurs(users: dict):
    with FICHIER_UTILISATEURS.open("w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def hash_mdp(mdp: str) -> str:
    return sha256(mdp.encode("utf-8")).hexdigest()

# En-tête
st.title("Créer votre compte")
st.write("Créez votre compte dès maintenant !")


st.divider()

# Formulaire de création de compte
prenom = st.text_input("Prénom")
nom = st.text_input("Nom")
email = st.text_input("Email")
mot_de_passe = st.text_input("Mot de passe", type="password")

st.write(" ")

# Cases à cocher
col1, col2 = st.columns(2)
with col1:
    cgu = st.checkbox("J'accepte les CGU et Politique de confidentialité")
with col2:
    info_mail = st.checkbox("Être informé des dernières activités par mail")

st.write(" ")

# Bouton de création de compte
if st.button("CRÉER MON COMPTE", use_container_width=True):
    if not prenom or not nom or not email or not mot_de_passe:
        st.warning("Veuillez remplir tous les champs.")
    elif not cgu:
        st.warning("Vous devez accepter les CGU pour continuer.")
    else:
        users = charger_utilisateurs()
        if email in users:
            st.error("Un compte avec cet email existe déjà. Veuillez vous connecter.")
        else:
            # Sauvegarde le compte
            users[email] = {
                "prenom": prenom,
                "nom": nom,
                "mot_de_passe": hash_mdp(mot_de_passe),
                "info_mail": info_mail
            }
            sauvegarder_utilisateurs(users)
            
            # Sauvegarde dans la session
            st.session_state.user = {
                "email": email,
                "prenom": prenom,
                "nom": nom
            }
            st.success(f"Bienvenue {prenom} ! Votre compte a été créé avec succès 🎉")
            
            # Redirection vers page de personnalisation
            st.switch_page("pages/mon_suivi.py")

st.write("---")

# Lien vers la connexion
st.write("Avez-vous déjà un compte ?")
if st.button("Se connecter", use_container_width=True):
        st.switch_page("pages/connexion.py")
