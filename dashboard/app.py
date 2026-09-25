import streamlit as st
from fonctions import charger_referentiel

st.set_page_config(
    page_title="Pilotage des files de jeu",
    layout="wide"
)

st.title("Pilotage des files de jeu")

referentiel = charger_referentiel()

# Les filtres sont conservés quand on change de page.
if "annee" not in st.session_state:
    st.session_state.annee = referentiel["annees"][-1]

if "serveur" not in st.session_state:
    st.session_state.serveur = "Tous"

if "jeu" not in st.session_state:
    st.session_state.jeu = "Tous"

if "file" not in st.session_state:
    st.session_state.file = "Toutes"

st.sidebar.title("Filtres")

st.session_state.annee = st.sidebar.selectbox(
    "Année",
    referentiel["annees"],
    index=referentiel["annees"].index(st.session_state.annee)
)

st.session_state.serveur = st.sidebar.selectbox(
    "Serveur",
    ["Tous"] + [s["code"] for s in referentiel["serveurs"]],
    index=(["Tous"] + [s["code"] for s in referentiel["serveurs"]]).index(
        st.session_state.serveur
    )
)

st.session_state.jeu = st.sidebar.selectbox(
    "Jeu",
    ["Tous"] + [j["nom"] for j in referentiel["jeux"]],
    index=(["Tous"] + [j["nom"] for j in referentiel["jeux"]]).index(
        st.session_state.jeu
    )
)

st.session_state.file = st.sidebar.selectbox(
    "File",
    ["Toutes"] + [f["nom"] for f in referentiel["files"]],
    index=(["Toutes"] + [f["nom"] for f in referentiel["files"]]).index(
        st.session_state.file
    )
)

st.sidebar.write("---")
st.sidebar.write("Les filtres restent conservés lorsque vous changez de page.")

st.write("Utilisez le menu à gauche pour accéder aux deux pages du tableau de bord.")
