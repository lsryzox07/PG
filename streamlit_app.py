
import streamlit as st
import pandas as pd
import os

# Chargement des images locales
image_dir = "images"
exercise_data = {
    "Développé couché": {"groupe": "Pectoraux", "image": "developpe_couche.jpg"},
    "Tractions": {"groupe": "Dos", "image": "tractions.jpg"},
    "Crunch": {"groupe": "Abdos", "image": "crunch.jpg"},
    "Presse": {"groupe": "Jambes", "image": "presse.jpg"},
    "Curl haltères": {"groupe": "Biceps", "image": "curl_haltere.jpg"},
    "Élévations latérales": {"groupe": "Épaules", "image": "elevations_laterales.jpg"},
    "Extensions mollets": {"groupe": "Mollets", "image": "extensions_mollets.jpg"},
    "Crunch à la poulie": {"groupe": "Abdos", "image": "crunch_poulie.jpg"},
    "Tirage horizontal": {"groupe": "Dos", "image": "tirage_horizontal.jpg"},
    "Dips": {"groupe": "Triceps", "image": "dips.jpg"},
    "Leg curl allongé": {"groupe": "Jambes", "image": "leg_curl_allonge.jpg"},
    "Chaise romaine": {"groupe": "Abdos", "image": "chaise_romaine.jpg"},
}

all_exercises = list(exercise_data.keys())

if "seances" not in st.session_state:
    st.session_state["seances"] = {j: [] for j in ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]}

st.set_page_config(page_title="Planificateur de Musculation", layout="centered")

st.markdown("## 🏋️‍♀️ **Planificateur d'Entraînement Personnalisé**")
st.markdown("Crée ta séance en choisissant tes exercices préférés. Ajoute des séries, des répétitions et visualise ton programme par jour.")

# Choix du jour
jour = st.selectbox("📅 Choisis un jour de la semaine :", list(st.session_state["seances"].keys()))

# Recherche exercice
search = st.text_input("🔍 Recherche un exercice").lower()
filtered = [e for e in all_exercises if search in e.lower()] if search else all_exercises

if filtered:
    selected_exo = st.selectbox("🏋️ Choisis un exercice :", filtered)
    exo_info = exercise_data[selected_exo]
    image_path = os.path.join(image_dir, exo_info["image"])
    if os.path.exists(image_path):
        st.image(image_path, caption=f"{selected_exo} – {exo_info['groupe']}", use_column_width=True)
    else:
        st.warning("Image manquante.")

    st.markdown("### 📊 Paramètres de l'exercice")
    cols = st.columns(3)
    with cols[0]:
        series = st.number_input("Séries", 1, 10, 3)
    with cols[1]:
        reps = st.number_input("Répétitions", 1, 30, 12)
    with cols[2]:
        charge = st.text_input("Charge", "Poids du corps")

    if st.button("➕ Ajouter cet exercice à la séance"):
        st.session_state["seances"][jour].append({
            "Groupe": exo_info["groupe"],
            "Exercice": selected_exo,
            "Séries": series,
            "Répétitions": reps,
            "Charge": charge
        })
        st.success(f"✅ {selected_exo} ajouté au programme du {jour} !")
else:
    st.info("Aucun exercice trouvé avec ce mot-clé.")

# Affichage de la séance du jour
st.markdown(f"## 📋 Séance du {jour}")
df = pd.DataFrame(st.session_state["seances"][jour])
if not df.empty:
    st.dataframe(df)
else:
    st.warning("Aucun exercice ajouté pour ce jour.")

# Export Excel
if st.button("💾 Exporter le programme complet (.xlsx)"):
    full_data = []
    for j, exos in st.session_state["seances"].items():
        for e in exos:
            full_data.append({"Jour": j, **e})
    pd.DataFrame(full_data).to_excel("programme_muscu.xlsx", index=False)
    st.success("✅ Exportation réussie : programme_muscu.xlsx")
