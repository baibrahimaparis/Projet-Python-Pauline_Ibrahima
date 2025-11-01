import streamlit as st
import pandas as pd
import datetime
from pathlib import Path

st.set_page_config(page_title="Suivi de Candidatures", layout="wide")

# Dossier de données
DATA_DIR = Path("donnees")
DATA_DIR.mkdir(exist_ok=True)

FICHIER_CANDIDATURES = DATA_DIR / "candidatures.csv"
FICHIER_ENTRETIEN = DATA_DIR / "notes_entretien.csv"

# Vérification que l'utilisateur est connecté 
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("⚠️ Veuillez vous connecter pour accéder à vos candidatures et notes.")
    st.write("Connectez-vous !")
    if st.button("Se connecter", use_container_width=True):
        st.switch_page("pages/connexion.py")
    st.stop()

USER_EMAIL = st.session_state.user["email"]

# Bouton déconnexion 
if st.sidebar.button("Se déconnecter", key="btn_logout"):
    st.session_state.user = None
    st.warning("Vous êtes déconnecté. Veuillez vous connecter ici :")
    st.markdown("[Se connecter](pages/connexion.py)")
    st.stop()

# Fonctions  pour sauvegarde et charge des fichiers
def charger_candidatures() -> pd.DataFrame:
    colonnes = ["Entreprise", "Poste", "Secteur", "Date de candidature",
                "Statut", "Date de réponse", "Notes", "Utilisateur"]
    if FICHIER_CANDIDATURES.exists():
        df = pd.read_csv(FICHIER_CANDIDATURES, parse_dates=["Date de candidature", "Date de réponse"], dayfirst=True)
        for c in colonnes:
            if c not in df.columns:
                df[c] = pd.NA
        return df[colonnes]
    return pd.DataFrame(columns=colonnes)

def sauvegarder_candidatures(df: pd.DataFrame) -> None:
    df_to_save = df.copy()
    df_to_save["Date de candidature"] = pd.to_datetime(df_to_save["Date de candidature"], errors="coerce").dt.date
    df_to_save["Date de réponse"] = pd.to_datetime(df_to_save["Date de réponse"], errors="coerce").dt.date
    df_to_save.to_csv(FICHIER_CANDIDATURES, index=False)

def charger_notes_entretien() -> pd.DataFrame:
    colonnes = ["email", "entreprise", "notes", "questions", "date"]
    if FICHIER_ENTRETIEN.exists():
        df = pd.read_csv(FICHIER_ENTRETIEN)
        for c in colonnes:
            if c not in df.columns:
                df[c] = pd.NA
        return df[colonnes]
    return pd.DataFrame(columns=colonnes)

def sauvegarder_notes_entretien(df: pd.DataFrame) -> None:
    df.to_csv(FICHIER_ENTRETIEN, index=False)

# Initialisation session
if "candidatures" not in st.session_state:
    st.session_state.candidatures = charger_candidatures()
if "notes_entretien" not in st.session_state:
    st.session_state.notes_entretien = charger_notes_entretien()

# Menu
page = st.sidebar.selectbox("Menu", [
    "Tableau de bord",
    "Ajouter une candidature",
    "Statistiques",
    "Préparation entretien"
])

# Pages
if page == "Tableau de bord":
    st.title("Tableau de bord")
    df_user = st.session_state.candidatures[st.session_state.candidatures["Utilisateur"] == USER_EMAIL]
    
    # Conversion des dates pour affichage
    for col in ["Date de candidature", "Date de réponse"]:
        if col in df_user.columns:
            df_user[col] = pd.to_datetime(df_user[col], errors='coerce').dt.strftime("%Y-%m-%d")
    
    st.dataframe(df_user)

    st.write("---")
    st.subheader("Accéder aux offres d'emploi")
    if st.button("Voir les offres d'emploi", key="btn_offres"):
        st.switch_page("pages/offres_emploi.py")

elif page == "Ajouter une candidature":
    st.title("➕ Ajouter une candidature")
    with st.form("form_ajout"):
        entreprise = st.text_input("Entreprise")
        poste = st.text_input("Poste")
        secteur = st.text_input("Secteur")
        date_cand = st.date_input("Date de candidature", datetime.date.today())
        statut = st.selectbox("Statut", ["envoyée", "en_revue", "entretien", "offre", "refus", "sans_réponse"])
        date_reponse = st.date_input("Date de réponse (si applicable)", value=None)
        notes = st.text_area("Notes")
        valider = st.form_submit_button("Ajouter")
        
        if valider:
            ligne = {
                "Entreprise": entreprise,
                "Poste": poste,
                "Secteur": secteur,
                "Date de candidature": pd.to_datetime(date_cand).date() if date_cand else pd.NA,
                "Statut": statut,
                "Date de réponse": pd.to_datetime(date_reponse).date() if date_reponse else pd.NA,
                "Notes": notes,
                "Utilisateur": USER_EMAIL
            }
            st.session_state.candidatures = pd.concat([st.session_state.candidatures, pd.DataFrame([ligne])], ignore_index=True)
            sauvegarder_candidatures(st.session_state.candidatures)
            st.success("✅ Candidature ajoutée et sauvegardée.")

    st.write("---")
    st.subheader("Accéder aux offres d'emploi")
    if st.button("Voir les offres d'emploi", key="btn_offres"):
        st.switch_page("pages/offres_emploi.py")

elif page == "Statistiques": # Taux de réponse, délai moyen de réponse, secteur qui répondent le plus vite
    st.title("Statistiques")
    df_user = st.session_state.candidatures[st.session_state.candidatures["Utilisateur"] == USER_EMAIL]
    
    if not df_user.empty:
        total = len(df_user)
        repondu = df_user[df_user["Statut"].isin(["entretien", "offre", "refus"])].shape[0]
        taux_reponse = round((repondu / total) * 100, 1)
        st.metric("Taux de réponse", f"{taux_reponse}%")
        
        df_local = df_user.copy()
        df_local["Date de candidature"] = pd.to_datetime(df_local["Date de candidature"], errors="coerce")
        df_local["Date de réponse"] = pd.to_datetime(df_local["Date de réponse"], errors="coerce")
        df_local["Délai"] = (df_local["Date de réponse"] - df_local["Date de candidature"]).dt.days
        delai_moyen = int(df_local["Délai"].dropna().mean()) if df_local["Délai"].notna().any() else 0
        st.metric("Délai moyen de réponse", f"{delai_moyen} jours")

        secteurs = df_local[df_local["Statut"].isin(["entretien", "offre", "refus"])].groupby("Secteur").size().sort_values(ascending=False)
        st.write("Secteurs qui répondent le plus :")
        if not secteurs.empty:
            st.bar_chart(secteurs)
        else:
            st.info("Aucune réponse enregistrée pour l'instant.")

        progression = min(100, int((repondu / total) * 100))
        st.progress(progression / 100)
        st.write(f"Score de progression : {progression}/100")
    else:
        st.info("Ajoutez des candidatures pour afficher les statistiques.")

    st.write("---")
    st.subheader("Accéder aux offres d'emploi")
    if st.button("Voir les offres d'emploi", key="btn_offres"):
        st.switch_page("pages/offres_emploi.py")

elif page == "Préparation entretien":
    st.title("Préparation d'entretien")

    st.subheader("Checklist")
    checklist_items = ["CV prêt", "Lettre personnalisée", "Portfolio", "Tenue prête", "Recherche sur l'entreprise effectuée"]
    for i, it in enumerate(checklist_items):
        st.checkbox(it, key=f"chk_{i}")

    st.write("---")
    st.subheader("Notes par entreprise")
    with st.form("form_note"):
        entreprise = st.text_input("Entreprise")
        texte_notes = st.text_area("Notes pour l'entretien / points à préparer")
        questions_prep = st.text_area("Questions à préparer (séparées par ; )")
        ajouter_note = st.form_submit_button("Ajouter la note")
        
        if ajouter_note:
            nouvelle_note = pd.DataFrame([{
                "email": USER_EMAIL,
                "entreprise": entreprise,
                "notes": texte_notes,
                "questions": ";".join([q.strip() for q in questions_prep.split(";") if q.strip()]),
                "date": datetime.date.today().isoformat()
            }])
            
            st.session_state.notes_entretien = pd.concat([st.session_state.notes_entretien, nouvelle_note], ignore_index=True)
            sauvegarder_notes_entretien(st.session_state.notes_entretien)
            st.success("Note ajoutée et sauvegardée ✅")

    # Affichage notes utilisateur
    notes_user = st.session_state.notes_entretien[st.session_state.notes_entretien["email"] == USER_EMAIL]
    if not notes_user.empty:
        st.dataframe(notes_user)
    else:
        st.info("Aucune note enregistrée pour l'instant.")

    st.write("---")
    st.subheader("Questions types 🎤")
    questions = [
        "Parlez-moi de vous",
        "Pourquoi ce poste ?",
        "Pourquoi notre entreprise ?",
        "Quelle est votre plus grande réussite ?",
        "Parlez d'un échec et de ce que vous en avez appris",
        "Comment gérez-vous le stress ?"
    ]
    for q in questions:
        st.write(f"- {q}")

    st.write("---")
    st.subheader("Accéder aux offres d'emploi")
    if st.button("Voir les offres d'emploi", key="btn_offres"):
        st.switch_page("pages/offres_emploi.py")
