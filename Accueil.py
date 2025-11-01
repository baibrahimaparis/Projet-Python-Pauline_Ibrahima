import streamlit as st
st.set_page_config(page_title="Accueil", layout="wide")

# On va centrer le conteneur du titre, de l'image et du bouton à l'avance grâce à HTML
st.markdown("""
<style>
h1 {
    text-align: center; 
}

div[data-testid="stVerticalBlock"] {
    gap: 1.5rem; 
    align-items: center; 
}

div.stButton {
    display: flex;
    justify-content: center;
}

div.stImage {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)



# CSS pour changer la couleur de fond
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background-color: #2773F5; }


    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Utilisation du système de colonne pour centrer les éléments
col_left, col_center, col_right = st.columns([1, 2, 1])
with col_center:
    st.title("First Xperience")
    st.write("") 
    st.image("image_accueil.png", width=400)
    if st.button("Commencer"):
        st.switch_page("pages/connexion.py")




