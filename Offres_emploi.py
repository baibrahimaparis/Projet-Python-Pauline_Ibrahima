import streamlit as st
import requests
import json

st.set_page_config(page_title="Offres d'emploi", layout="centered")

# Lien vers "Mon suivi"
if st.button("Retour à Mon suivi"):
    st.switch_page("pages/Mon_suivi.py")  

# Input pour rechercher un poste
poste_recherche = st.text_input("Quel poste recherchez-vous ?")

# Bouton pour lancer la recherche
if st.button("Chercher les offres"):
    if not poste_recherche.strip():
        st.warning("Veuillez saisir un intitulé de poste.")
    else:
        # Récupérer les valeurs de RapidAPI (jAPI)
        API_KEY = "c25f4608c4msh1d911de9bb64b3fp12c929jsn06706ad906e0" 
        HOST = "jsearch.p.rapidapi.com"
        URL = "https://jsearch.p.rapidapi.com/search"

        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": HOST
        }

        params = {
            "query": poste_recherche,  
            "page": "1",
            "num_pages": "1"
        }

        try:
            response = requests.get(URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()

            if data and data.get("data"):
                st.success(f"Nombre d'offres trouvées : {len(data['data'])}")

                for job in data['data']:
                    st.markdown(f"### {job.get('job_title', 'Titre non spécifié')}")
                    st.write(f"**Entreprise :** {job.get('employer_name', 'N/A')} - **Lieu :** {job.get('job_city', 'N/A')}")
                    st.markdown(f"[Voir l'offre]({job.get('job_apply_link')})")
                    st.divider()
            else:
                st.info("Aucune offre trouvée pour cette recherche.")

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de connexion à l'API : {e}")
        except Exception as e:
            st.error(f"Une erreur inattendue s'est produite : {e}")
