
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Mamba Admin v1", page_icon="🤖", layout="centered")

st.title("🤖 Mamba Admin v1")
st.caption("Votre assistant administratif virtuel tout-en-un")

SYSTEM_PROMPT = """
Tu es "Mamba Admin v1", un Assistant Administratif Virtuel Tout-en-un.
Tu as 3 modes de fonctionnement :
1. Relance de Facture (Génère un e-mail d'impayé adapté)
2. Tri et Évaluation de CV (Analyse un CV par rapport à un poste)
3. Filtre & Réponse d'E-mail (Traite un e-mail complexe et rédige un brouillon)

Si l'utilisateur ne précise pas le mode, demande-lui de choisir entre 1, 2 ou 3.
Sois toujours professionnel, rigoureux et précis.
"""

# Barre latérale pour la clé API
api_key = st.sidebar.text_input("Clé API OpenAI :", type="password")

if not api_key:
    st.info("💡 Veuillez entrer votre clé API OpenAI dans le panneau de gauche pour commencer.")
    st.stop()

# Initialisation du client OpenAI
client = OpenAI(api_key=api_key)

# Gestion de la session de messagerie
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "👋 Bienvenue dans votre Assistant Mamba Admin v1 !\n\nVeuillez choisir un mode :\n1️⃣ **Relance de Facture**\n2️⃣ **Tri et Évaluation de CV**\n3️⃣ **Filtre & Réponse d'E-mail**\n\nTapez le numéro (1, 2 ou 3) ou décrivez votre besoin."}
    ]

# Affichage de l'historique
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Envoi de message
if user_input := st.chat_input("Écrivez votre message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages
        )
        bot_reply = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)
    except Exception as e:
        st.error(f"Erreur API : {e}")
