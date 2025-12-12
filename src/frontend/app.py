import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Ladda env-variabler (.env)
load_dotenv()

# Azure Function URL + Function Key (samma mönster som läraren)
API_URL = f"http://localhost:7071/rag?code={os.getenv('FUNCTION_APP_API')}"
# När deployad:
# API_URL = f"https://rag-youtuber-said.azurewebsites.net/api/rag?code={os.getenv('FUNCTION_APP_API')}"

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="RAG Course Assistants",
    page_icon="🤖",
    layout="centered",
)

# -------------------------------
# Custom Dark Theme CSS
# -------------------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #FFFFFF;
}

h1 {
    color: #00C4FF !important;
    text-align: center;
}

.stTextInput > div > div > input {
    background-color: #1A1F27;
    color: #FFFFFF;
    border: 1px solid #00C4FF;
    border-radius: 8px;
    padding: 10px;
}

.stButton > button {
    background-color: #00C4FF;
    color: black;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}

.stButton > button:hover {
    background-color: #05D6FF;
}

.chat-bubble-user {
    background-color: #1F2937;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #FFFFFF;
}

.chat-bubble-ai {
    background-color: #0EA5E9;
    padding: 12px 16px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #FFFFFF;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# UI HEADER
# -------------------------------
st.markdown("<h1>🤖 Said RAG Assistant</h1>", unsafe_allow_html=True)
st.write("AI-assistenten söker igenom kursens material och svarar direkt på dina frågor.")

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.text_input("", placeholder="Skriv din fråga här...")
send = st.button("Skicka")

# -------------------------------
# HANDLE REQUEST
# -------------------------------
if send and user_input.strip() != "":
    with st.spinner("Hämtar svar..."):
        response = requests.post(API_URL, json={"query": user_input})

        if response.status_code == 200:
            data = response.json()

            # User bubble
            st.markdown(
                f"<div class='chat-bubble-user'>🧑‍💻 {user_input}</div>",
                unsafe_allow_html=True
            )

            # AI bubble
            st.markdown(
                f"<div class='chat-bubble-ai'>🤖 {data['answer']}</div>",
                unsafe_allow_html=True
            )

            # Sources
            st.subheader("📚 Källor")
            for src in data["sources"]:
                st.write(f"- {src}")
        else:
            st.error("API-anropet misslyckades. Kontrollera Function Key och backend.")
