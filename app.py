Python
import streamlit as st
import openai

# Configuration de la page Streamlit
st.set_page_config(page_title="Mamba Admin v1", page_icon="🤖", layout="centered")

st.title("🤖 Mamba Admin v1")
st.caption("Votre assistant administratif virtuel tout-en-un")

# Insérer le System Prompt de Mamba Admin
SYSTEM_PROMPT = """
Tu es "Mamba Admin v1", un Assistant Administratif Virtuel Tout-en-un.
Tu as 3 modes de fonctionnement :
1. Relance de Facture (Génère un e-mail d'impayé adapté)
2. Tri et Évaluation de CV (Analyse un CV par rapport à un poste)
3. Filtre & Réponse d'E-mail (Traite un e-mail complexe et rédige un brouillon)

Si l'utilisateur ne précise pas le mode, demande-lui de choisir entre 1, 2 ou 3.
Sois toujours professionnel, rigoureux et précis.
"""

# Clé API OpenAI (à renseigner dans Streamlit Secrets ou champ texte)
api_key = st.sidebar.text_input("Clé API OpenAI :", type="password")

if not api_key:
    st.info("💡 Veuillez entrer votre clé API OpenAI dans le panneau de gauche pour commencer.")
    st.stop()

openai.api_key = api_key

# Historique de chat
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "👋 Bienvenue dans votre Assistant Mamba Admin v1 !\n\nVeuillez choisir un mode :\n1️⃣ **Relance de Facture**\n2️⃣ **Tri et Évaluation de CV**\n3️⃣ **Filtre & Réponse d'E-mail**\n\nTapez le numéro (1, 2 ou 3) ou décrivez votre besoin."}
    ]

# Affichage des messages (hors system)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

# Entrée de l'utilisateur
if user_input := st.chat_input("Écrivez votre message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Appel à l'API OpenAI
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )
    
    bot_reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.chat_message("assistant").write(bot_reply)
