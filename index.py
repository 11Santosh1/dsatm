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
labels = {
    "English": {
        "edu_advice": "📚 Get advice in specific education categories",
        "choose_category": "Choose a Category:",
        "ask_question": "Career Guidance / real time study evalution",
        "get_answer": "Get Answer",
        "warning": "Please enter a question.",
        "generating": "Generating response...",
        "answer": "Answer:"
    },
    
    "ಕನ್ನಡ": {
        "edu_advice": "📚 ನಿರ್ದಿಷ್ಟ ಶಿಕ್ಷಣ ವರ್ಗಗಳಲ್ಲಿ ಸಲಹೆ ಪಡೆಯಿರಿ",
        "choose_category": "ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "ask_question": "ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:",
        "get_answer": "ಉತ್ತರವನ್ನು ಪಡೆಯಿರಿ",
        "warning": "ದಯವಿಟ್ಟು ಪ್ರಶ್ನೆಯನ್ನು ನಮೂದಿಸಿ.",
        "generating": "ಉತ್ತರವನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...",
        "answer": "ಉತ್ತರ:"
    },
    "E-book": {
    "edu_advice": "📘 ಇ-ಪುಸ್ತಕವನ್ನು ಓದಿ ಮತ್ತು ಕಲಿಯಿರಿ",
    "choose_category": "ಇ-ಪುಸ್ತಕ ವಿಭಾಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
    "ask_question": "ಈ ಇ-ಪುಸ್ತಕ ಕುರಿತು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:",
    "get_answer": "ಉತ್ತರ ಪಡೆಯಿರಿ",
    "warning": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ನಮೂದಿಸಿ.",
    "generating": "ಉತ್ತರವನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...",
    "answer": "ಉತ್ತರ:"
    },
    "Podcast": {
    "edu_advice": "🎧 ಶೈಕ್ಷಣಿಕ ಪೋಡ್‌ಕಾಸ್ಟ್‌ಗಳನ್ನು ಕೇಳಿ",
    "choose_category": "ಪೋಡ್‌ಕಾಸ್ಟ್ ವಿಭಾಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
    "ask_question": "ಈ ಪೋಡ್‌ಕಾಸ್ಟ್ ಕುರಿತು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಕೇಳಿ:",
    "get_answer": "ಉತ್ತರ ಪಡೆಯಿರಿ",
    "warning": "ದಯವಿಟ್ಟು ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ನಮೂದಿಸಿ.",
    "generating": "ಉತ್ತರವನ್ನು ರಚಿಸಲಾಗುತ್ತಿದೆ...",
    "answer": "ಉತ್ತರ:"
    }
}

if mode == "Science Chatbot for Kids":
    if "science_chat" not in st.session_state:
        st.session_state.science_chat = science_model.start_chat(history=[])

   

    # Show chat history
    for msg in st.session_state.science_chat.history:
        with st.chat_message("user" if msg.role == "user" else "assistant"):
            st.markdown(msg.parts[0].text)

    # Chat input
    user_input = st.chat_input("Ask me anything science-y!")

    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        response = st.session_state.science_chat.send_message(user_input)

        with st.chat_message("assistant"):
            st.markdown(response.text)
#added chats
else:
    st.subheader(labels[mode]["edu_advice"])

    category = st.selectbox(labels[mode]["choose_category"], ["", "Primary", "High School", "PUC", "Engineering", "Finance", "MBBS"])
    user_prompt = st.text_area(labels[mode]["ask_question"])

    if st.button(labels[mode]["get_answer"]):
        if not user_prompt.strip():
            st.warning(labels[mode]["warning"])
        else:
            with st.spinner(labels[mode]["generating"]):
                reply = get_gemini_response(user_prompt, category)
                st.success(labels[mode]["answer"])
                st.markdown(reply)


if "public_key" not in st.session_state:
    public_key, private_key = paillier.generate_paillier_keypair()
    st.session_state.public_key = public_key
    st.session_state.private_key = private_key

if "encrypted_transactions" not in st.session_state:
    st.session_state.encrypted_transactions = {}

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

if "wallet" not in st.session_state:
    st.session_state.wallet = []
if "last_passkey_change_time" not in st.session_state:
    st.session_state.last_passkey_change_time = time.time()
#used timer sequence
if "encryption_method" not in st.session_state:
    st.session_state.encryption_method = "HE"

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "pan_no" not in st.session_state:
    st.session_state.pan_no = ""


def encrypt_data(data):
    if st.session_state.encryption_method == "HE":
        encrypted_data = st.session_state.public_key.encrypt(float(data))
    elif st.session_state.encryption_method == "FFHE":
        encrypted_data = encrypt_data_fhe(data)
    return encrypted_data

#added to states
def decrypt_data(encrypted_data):
    if st.session_state.encryption_method == "HE":
        return st.session_state.private_key.decrypt(encrypted_data)
    elif st.session_state.encryption_method == "FFHE":
        return decrypt_data_fhe(encrypted_data)

def encrypt_data_fhe(data):
    return data


def decrypt_data_fhe(encrypted_data):
    return encrypted_data


def get_current_passkey():
    elapsed_time = time.time() - st.session_state.last_passkey_change_time
    if elapsed_time > 300:
        st.session_state.last_passkey_change_time = time.time()
        return "sit4321" if (int(elapsed_time / 300) % 2 == 1) else "sit1234"
    else:
        return "sit1234" if (int(elapsed_time / 300) % 2 == 0) else "sit4321"


def display_countdown():
    elapsed_time = time.time() - st.session_state.last_passkey_change_time
    remaining_time = 300 - elapsed_time
    if remaining_time > 0:
        st.write(f"Time until next passkey change: {int(remaining_time)} seconds")
    else:
        st.write("Passkey has been updated!")


def check_network_traffic():
    network_stats = psutil.net_io_counters()
    bytes_sent = network_stats.bytes_sent / (1024 * 1024)
    bytes_recv = network_stats.bytes_recv / (1024 * 1024)
    total_network_traffic = bytes_sent + bytes_recv
    return total_network_traffic

network_traffic = check_network_traffic()
suspicious_activity = False
if suspicious_activity:
    st.markdown(
        '<p style="color:red; text-align:center; font-size:20px; font-weight:bold;">⚠️ Suspicious network activity detected! ⚠️</p>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<p style="color:green; text-align:center; font-size:20px; font-weight:bold;">✔️ No suspicious activity detected.</p>',
        unsafe_allow_html=True
    )

st.write(f"Total Network Traffic: {network_traffic:.2f} MB")


st.title("SAHAYOGI – Empowering Rural Education")
st.write("Welcome to the platform where learning meets innovation for every rural student")
read_aloud_button()

if "nav_section" not in st.session_state:
    st.session_state.nav_section = "Home"


def navigate_to(section):
    st.session_state.nav_section = section

st.sidebar.markdown("<h2 style='text-align: center;'>🔍 Even those who are considered the most immoral of all sinners can cross over this ocean of material existence by seating themselves in the boat of divine knowledge.<br><br>Micro challenge:Can you name five objects around you that start with the first five English letters?</h2>", unsafe_allow_html=True)

st.markdown("## 🎙️ Speak to Ask a Question")

# Embed the speech-to-text HTML + JavaScript
components.html("""
  <html>
    <body>
      <div style="text-align: center;">
        <button onclick="startListening()" style="
            font-size: 20px;
            padding: 12px 24px;
            background-color: #34A853;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
          🎤 Speak Now
        </button>
        <p id="result" style="font-size: 18px; margin-top: 20px;"></p>
      </div>

      <script>
        function startListening() {
          const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
          recognition.lang = 'en-US';
          recognition.interimResults = false;
          recognition.maxAlternatives = 1;

          recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('result').innerText = "🗣️ You said: " + transcript;

            // Append the spoken text to the URL query string
            const newURL = window.location.protocol + "//" + window.location.host + window.location.pathname + '?text=' + encodeURIComponent(transcript);
            window.location.href = newURL;
          };

          recognition.onerror = function(event) {
            document.getElementById('result').innerText = " Error: " + event.error;
          };

          recognition.start();
        }
      </script>
    </body>
  </html>
""", height=300)

# Use the new st.query_params
spoken_text = st.query_params.get("text", "")

if spoken_text:
    st.success(f"✅ You said: {spoken_text}")

button_style = """
    <style>
    div.stButton > button {
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 0.75em 1.2em;
        margin-bottom: 0.5em;
        width: 100%;
        border-radius: 8px;
        background-color: orange;
    }
    </style>
"""
st.sidebar.markdown(button_style, unsafe_allow_html=True)

st.sidebar.header("Navigation")
nav_map = {
    "Primary": "Primary",
    "Higher Studies": "Higher Studies",
    
    "Home": "Home",
    "FAQ's": "FAQ's",
    "Support": "Support",
    "Settings": "Settings",
    "Graph Chart": "Graph Chart",
    "Spending Analysis": "Spending Analysis",
    "Encrypted Data": "Encrypted Data",
    "Wallet": "Wallet",
    "Credential Encryption": "Credential Encryption", 
    "Withdraw": "Withdraw", 
    "Logout": "Logout",
}

nav_labels_local = nav_labels[mode]

for key, value in nav_map.items():
    if st.sidebar.button(nav_labels_local[key]):
        navigate_to(value)




nav_section = st.session_state.nav_section



if nav_section == "Home":
    st.header("Home")

    if not st.session_state.user_authenticated:
        st.subheader("User Authentication")
        user_password = st.text_input("Enter User Passkey:", type="password")

        if st.button("Authenticate User"):
            if user_password == "user123":
                st.session_state.user_authenticated = True
                st.success("User authenticated successfully!")
            else:
                st.error("Invalid passkey! Please try again.")

    if st.session_state.user_authenticated:
        section = st.selectbox("Select Section", ["User Section", "Admin Section"])

        if section == "User Section":
            st.subheader("Submit Financial Data")

            st.session_state.user_id = st.text_input("Enter User ID:", value=st.session_state.user_id)
            st.session_state.pan_no = st.text_input("Enter PAN Number:", value=st.session_state.pan_no)
            transaction_amount = st.text_input("Enter Transaction Amount (numeric):")

            if not transaction_amount:
                transaction_amount = '0000'

            current_passkey = get_current_passkey()
            display_countdown()
            passkey = st.text_input("Enter Passkey:", type="password")

            if st.button("Encrypt and Submit"):
                if st.session_state.user_id and st.session_state.pan_no and transaction_amount.replace('.', '', 1).isdigit() and passkey == current_passkey:
                    encrypted_data = encrypt_data(transaction_amount)
                    st.session_state.encrypted_transactions[st.session_state.user_id] = encrypted_data

                    st.session_state.transaction_history.append({
                        "user_id": st.session_state.user_id,
                        "pan_no": st.session_state.pan_no,
                        "transaction_amount": transaction_amount,
                        "status": "Encrypted and stored securely"
                    })

                    st.session_state.wallet.append({
                        "amount": float(transaction_amount),
                        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    })

                    st.success("Transaction encrypted and stored securely!")
                elif passkey != current_passkey:
                    st.error("Invalid passkey! Please try again.")
                else:
                    st.error("Please enter valid transaction data.")
#HE updated
            st.subheader("Transaction History")
            if st.session_state.transaction_history:
                for idx, transaction in enumerate(st.session_state.transaction_history, 1):
                    st.write(f"{idx}. User ID: {transaction['user_id']}, PAN No: {transaction['pan_no']}, Amount: {transaction['transaction_amount']}, Status: {transaction['status']}")
            else:
                st.write("No transactions submitted yet.")

        elif section == "Admin Section":
            st.subheader("Admin Panel")
            admin_password = st.text_input("Enter Admin Access Code:", type="password")
            if st.button("Access Admin Panel"):
                if admin_password == "admin123":
                    st.success("Access granted!")
                    if st.session_state.encrypted_transactions:
                        st.write("### Decrypted Financial Transactions")
                        for user, encrypted_data in st.session_state.encrypted_transactions.items():
                            try:
                                decrypted_amount = decrypt_data(encrypted_data)
                                st.write(f"**User ID:** {user}, **Transaction Amount:** {decrypted_amount}")
                            except ValueError as e:
                                st.error(f"Error decrypting data for User ID {user}: {e}")
                    else:
                        st.info("No transactions to display.")
                else:
                    st.error("Incorrect access code! Access denied.")
