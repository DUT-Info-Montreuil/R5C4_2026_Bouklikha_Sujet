import streamlit as st
from fonctions import charger_indicateurs

st.title("Indicateurs")

donnees = charger_indicateurs()

annee = st.session_state.get("annee", "2025")

# À cette séance, les indicateurs viennent directement de la fixture.
donnees_annee = donnees[annee]

st.write(
    f"Comparaison entre {donnees_annee['periode']} "
    f"et {donnees_annee['periode_reference'] or 'aucune année précédente'}"
)

colonnes = st.columns(3)

for colonne, indicateur in zip(colonnes, donnees_annee["indicateurs"]):
    with colonne:
        valeur = indicateur["valeur"]
        reference = indicateur["reference"]
        ecart = indicateur["ecart"]

        if indicateur["unite"] == "parties":
            valeur_affichee = f"{valeur:,.0f}".replace(",", " ")
        elif indicateur["unite"] == "secondes":
            valeur_affichee = f"{valeur:.2f} s"
        else:
            valeur_affichee = f"{valeur:.2f} min"

        if ecart is None:
            delta = None
        else:
            delta = f"{ecart * 100:+.2f} %"

        st.metric(
            label=indicateur["nom"],
            value=valeur_affichee,
            delta=delta
        )

        if reference is not None:
            st.caption(
                f"Référence : {reference} {indicateur['unite']}"
            )
        else:
            st.caption("Pas de référence pour la première année.")

        if indicateur["sens"] == "hausse_favorable":
            st.caption("Une hausse est favorable.")
        else:
            st.caption("Une hausse est défavorable.")
