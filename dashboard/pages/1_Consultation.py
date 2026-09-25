import streamlit as st
from fonctions import charger_parties

st.title("Consultation des parties")

donnees = charger_parties()
parties = donnees["data"]

# Récupération des filtres communs
annee = st.session_state.get("annee")
serveur = st.session_state.get("serveur", "Tous")
jeu = st.session_state.get("jeu", "Tous")
file = st.session_state.get("file", "Toutes")

# Les fixtures permettent de tester ces filtres localement.
parties_filtrees = []

for partie in parties:
    if annee and partie["debut"][:4] != annee:
        continue

    if serveur != "Tous" and partie["serveur"] != serveur:
        continue

    if jeu != "Tous" and partie["jeu"] != jeu:
        continue

    if file != "Toutes" and partie["file"] != file:
        continue

    parties_filtrees.append(partie)

total = len(parties_filtrees)
taille_page = 20
nombre_pages = max(1, (total + taille_page - 1) // taille_page)

if "page" not in st.session_state:
    st.session_state.page = 1

if st.session_state.page > nombre_pages:
    st.session_state.page = 1

debut = (st.session_state.page - 1) * taille_page
fin = debut + taille_page

parties_page = parties_filtrees[debut:fin]

st.write(f"Parties correspondant aux filtres : {total}")

if parties_page:
    st.dataframe(
        parties_page,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Aucune partie ne correspond aux filtres sélectionnés.")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Précédent"):
        if st.session_state.page > 1:
            st.session_state.page -= 1
            st.rerun()

with col2:
    st.write(f"Page {st.session_state.page} / {nombre_pages}")

with col3:
    if st.button("Suivant →"):
        if st.session_state.page < nombre_pages:
            st.session_state.page += 1
            st.rerun()
