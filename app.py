import streamlit as st
from google import genai

st.set_page_config(
    page_title="Tuteur Scolaire", page_icon="🎓", layout="centered"
)

st.title("🎓 Mon Tuteur Scolaire")
st.write(
    "Pose ta question ou partage ton exercice, je suis là pour t'aider pas à"
    " pas !"
)

# Demander la clé API Gemini
api_key = st.text_input(
    "Entrez votre clé API Google Gemini :", type="password"
)

if api_key:
  client = genai.Client(api_key=api_key)

  system_instruction = (
      "Tu es un tuteur scolaire bienveillant et pédagogue. Ton rôle est d'aider"
      " les élèves à comprendre leurs leçons et leurs exercices en les guidant"
      " pas à pas avec des explications claires et des questions d'orientation,"
      " sans jamais donner directement la réponse finale."
  )

  if "messages" not in st.session_state:
    st.session_state.messages = []

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if prompt := st.chat_input("Écris ta question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
      st.markdown(prompt)

    with st.chat_message("assistant"):
      full_prompt = (
          f"{system_instruction}\n\nHistorique / Question de l'élève : {prompt}"
      )
      response = client.models.generate_content(
          model="gemini-2.5-flash", contents=full_prompt
      )
      st.markdown(response.text)
      st.session_state.messages.append(
          {"role": "assistant", "content": response.text}
      )
else:
  st.info("Veuillez entrer votre clé API Gemini ci-dessus pour commencer.")
      
