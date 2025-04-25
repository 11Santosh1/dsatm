import streamlit as st
from phe import paillier
import time
import matplotlib.pyplot as plt
import numpy as np
import psutil
from cryptography.fernet import Fernet  # For file-based encryption
import google.generativeai as genai
from gtts import gTTS
import streamlit.components.v1 as components
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import base64

GOOGLE_API_KEY = "AIzaSyDDmTosHLLulk4lId8Xj1LFBWh-OyjSci0"
genai.configure(api_key=GOOGLE_API_KEY)

# Model configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Science-focused model setup
science_model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=(
        "You are an expert at teaching science to kids. Your task is to engage in conversations "
        "about science and answer questions. Explain scientific concepts so that they are easily "
        "understandable. Use analogies and examples that are relatable. Use humor and make the "
        "conversation both educational and interesting. Ask questions so that you can better "
        "understand the user and improve the educational experience. Suggest ways that these concepts "
        "can be related to the real world with observations and experiments."
    )
)
def read_aloud_button():
    read_aloud_html = """
    <script>
        function readScreenText() {
            const allText = document.body.innerText;
            const utterance = new SpeechSynthesisUtterance(allText);
            speechSynthesis.speak(utterance);
        }
    </script>
    <button onclick="readScreenText()" style="font-size:20px; padding:10px 20px; background-color:lightblue; border:none; border-radius:8px;">🔈 SOS</button>
    """
    components.html(read_aloud_html, height=100)


def play_audio(letter):
    audio_html = f"""
    <audio id="{letter}_audio" src="/static/police-siren-sound-effect-317645.mp3"></audio>
    <script>
        const button = document.getElementById("{letter}_button");
        if (button) {{
            button.onclick = () => {{
                const audio = document.getElementById("{letter}_audio");
                audio.play();
            }};
        }}
    </script>
    <button id="{letter}_button" style="font-size:24px;">🔊 {letter}</button>
    """
    components.html(audio_html, height=100)





# 🧠 Generic educational model for category-based advice
def get_gemini_response(prompt, category=None):
    generic_model = genai.GenerativeModel("gemini-1.5-pro")
    full_prompt = f"You are an educational advisor. {f'Focus on {category} education.' if category else ''} Answer this: {prompt}"
    try:
        response = generic_model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI Setup
st.set_page_config(page_title="SAHAYOGI", page_icon="🧠", layout="wide")


# Mode selector
mode = st.radio("Language / ಭಾಷೆ", ["English", "ಕನ್ನಡ", "E-book", "Podcast"], horizontal=True)

if mode == "Podcast":
    st.markdown("### 🎙️ Listen to Our Latest Podcast")

    # Read the local MP3 file
    file_path = "shloka.mp3"
    with open(file_path, "rb") as f:
        audio_data = f.read()
        base64_audio = base64.b64encode(audio_data).decode("utf-8")

    # Embed the audio player using HTML
    audio_player = f'''
        <audio controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{base64_audio}" type="audio/mpeg">
            Your browser does not support the audio element.
        </audio>
    '''
    st.markdown(audio_player, unsafe_allow_html=True)

if mode == "E-book":
    st.markdown("### 📘 E-book Viewer")

    # Read the local PDF file
    file_path = "IEEE.pdf"
    with open(file_path, "rb") as f:
        pdf_data = f.read()
        base64_pdf = base64.b64encode(pdf_data).decode("utf-8")

    # Correct iframe with base64-encoded PDF using data URI
    pdf_display = f'''
        <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>
    '''
    st.markdown(pdf_display, unsafe_allow_html=True)

    # Download button
    st.download_button(
        label="📥 Download E-book",
        data=pdf_data,
        file_name="ebook.pdf",
        mime="application/pdf"
    )
nav_labels = {
    "English": {
        "Primary": "Primary",
        "Higher Studies": "Higher Studies",
        "Home": "Finance",
        "FAQ's": "FAQ's",
        "Support": "Support",
        "Settings": "Settings",
        "Graph Chart": "Graph Chart",
        "Spending Analysis": "Spending Analysis",
        "Encrypted Data": "Encrypted Data",
        "Wallet": "Wallet",
        "Credential Encryption": "Credential Encryption",
        "Withdraw": "Withdraw",
        "Logout": "Logout"
    },
    "ಕನ್ನಡ": {
        "Primary": "ಪ್ರಾಥಮಿಕ",
        "Higher Studies": "ಉನ್ನತ ಅಧ್ಯಯನ",
        "Home": "ಹಣಕಾಸು",
        "FAQ's": "ಸಮಸ್ಯೆಗಳು",
        "Support": "ಬೆಂಬಲ",
        "Settings": "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
        "Graph Chart": "ಗ್ರಾಫ್ ಚಾರ್ಟ್",
        "Spending Analysis": "ಖರ್ಚು ವಿಶ್ಲೇಷಣೆ",
        "Encrypted Data": "ಎನ್ಕ್ರಿಪ್ಟ್ ಡೇಟಾ",
        "Wallet": "ವಾಲೆಟ್",
        "Credential Encryption": "ಪ್ರಮಾಣಪತ್ರ ಎನ್ಕ್ರಿಪ್ಷನ್",
        "Withdraw": "ಹಿಂತೆಗೆದುಕೊಳ್ಳಿ",
        "Logout": "ಲಾಗ್ ಔಟ್"
    }
}
