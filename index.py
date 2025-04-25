#for DSATM hackathon by team CODESMITHS...Had a wonderfull experience
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
import streamlit.components.v1 as components

GOOGLE_API_KEY = "AIzaSyCpFbHXnYS0nxy7rBTiTwGwexfO75lqxSs"
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
st.set_page_config(page_title="SAHAYOG", page_icon="🧠", layout="wide")


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
        "Primary": "Primary 'SDG'",
        "Higher Studies": "Higher Studies with 'SDG'",
        "Home": "Sustainable Finance",
        "FAQ's": "Earn SDG badge",
        "Support": "Carbon Footprint Tracker",
        "Settings": "Settings",
        "Graph Chart": "Graph Chart",
        "Spending Analysis": "Spending Analysis",
        "Encrypted Data": "Encrypted Data",
        "Wallet": "Wallet",
        "Credential Encryption": "SDG News",
        "Withdraw": "Withdraw",
        "Logout": "SDG AR Experience"
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
#adding labels
labels = {
    "English": {
        "edu_advice": "📚 Get advice in specific SDG education categories",
        "choose_category": "Choose a Category:",
        "ask_question": "Career Guidance / real time study evalution with SUSTAINABLE DEVELOPMENT GOALS",
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


st.title("SAHAYOG – Integrating SDG with Education")
st.write("Welcome to the platform where learning meets innovation for every rural student")

# Add floating growing tree
components.html("""
<style>
#tree-container {
    position: fixed;
    top: 10px;
    right: 20px;
    z-index: 9999;
}
#tree-img {
    width: 150px; /* Fixed large size */
    transition: opacity 0.6s ease-in-out;
    cursor: pointer;
}
</style>

<div id="tree-container">
    <img id="tree-img" src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse3.explicit.bing.net%2Fth%3Fid%3DOIP.grrBccEGYSMdW7ZE-WshkwHaF-%26cb%3Diwc1%26pid%3DApi&f=1&ipt=27d26934722166727a6e145b0a2021b610e4af5ce76d52f4706ec9230cd05fc9&ipo=images" alt="Tree" onclick="growTree()" />
</div>

<script>
let grown = false;

function growTree() {
    if (grown) return;

    const tree = document.getElementById("tree-img");

    // Smooth fade transition
    tree.style.opacity = 0;
    setTimeout(() => {
        tree.src = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse2.mm.bing.net%2Fth%3Fid%3DOIP.lxt54IaUvOtGM97XFgCcEAHaE7%26pid%3DApi&f=1&ipt=6da0211b3bb71e94e748ec52d84e5c2a54262444076ea4ae0ae82735d5aaee09&ipo=images";
        tree.style.opacity = 1;
    }, 300);

    grown = true;
}

// Automatically grow (change image) after 30 seconds
setTimeout(growTree, 30000);
</script>
""", height=200)







read_aloud_button()

if "nav_section" not in st.session_state:
    st.session_state.nav_section = "Home"


def navigate_to(section):
    st.session_state.nav_section = section



st.sidebar.markdown("<h2 style='text-align: center;'>🔍 Even those who are considered the most immoral of all sinners can cross over this ocean of material existence by seating themselves in the boat of divine knowledge.<br><br>Micro challenge:Can you name three ways you can reduce waste in your daily life starting today?</h2>", unsafe_allow_html=True)

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
    "Support": "Carbon Footprint Tracker",
    "Settings": "Settings",
    "Graph Chart": "Graph Chart",
    "Spending Analysis": "Spending Analysis",
    "Encrypted Data": "Encrypted Data",
    "Wallet": "Wallet",
    "Credential Encryption": "SDG News", 
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

# elif nav_section == "Higher Studies":
#     st.header("🎓 Higher Studies Section")
#     st.write("This section includes educational guidance for High School, PUC, Engineering, Finance, and MBBS students.")

#     categories = ["High School", "PUC", "Engineering", "Finance", "MBBS"]
#     selected_category = st.selectbox("Select Category", categories)

#     user_question = st.text_input("Ask your question:")
#     if st.button("Get Answer"):
#         if user_question:
#             with st.spinner("Thinking..."):
#                 # Use your Gemini API call here
#                 answer = get_gemini_response(user_question, selected_category)
#                 st.success("Response:")
#                 st.write(answer)
#         else:
#             st.warning("Please enter a question.")


elif nav_section == "Primary":
    if "page" not in st.session_state:
        st.session_state.page = "primary"

    if st.session_state.page == "primary":
        st.header("Primary Section")
        st.write("Welcome to the Primary Education Content Section.")

        st.markdown("""
        ### 🧠 Learn Basic Concepts of SDG
        - **Alphabets** (A-Z)
        - **Numbers** (1-100)
        - **Colors & Shapes**
        - **Basic Addition/Subtraction**
        - **No Poverty**
        - **End poverty in all its forms everywhere**
- **Zero Hunger**
        - **End hunger, achieve food security, and promote sustainable agriculture**
- **Good Health and Well-being**
        - **Ensure healthy lives and promote well-being for all**
- **Quality Education**
        - **Ensure inclusive and equitable education for all**
- **Gender Equality**
        - **Achieve gender equality and empower all women and girls**
- **Clean Water and Sanitation**
        - **Ensure availability and sustainable management of water and sanitation**
- **Affordable and Clean Energy**
        - **Ensure access to sustainable and modern energy**
- **Decent Work and Economic Growth**
        - **Promote sustained economic growth and productive employment**
- **Industry, Innovation, and Infrastructure**
        - **Build resilient infrastructure and promote innovation**
- **Reduced Inequalities**
        - **Reduce inequality within and among countries**
- **Sustainable Cities and Communities**
        - **Make cities inclusive, safe, and sustainable**
- **Responsible Consumption and Production**
        - **Ensure sustainable consumption and production patterns**
- **Climate Action**
        - **Take urgent action to combat climate change**
- **Life Below Water**
        - **Conserve oceans and marine resources**
- **Life on Land**
        - **Protect terrestrial ecosystems and halt biodiversity loss**
- **Peace, Justice and Strong Institutions**
        - **Promote peaceful societies and access to justice**
- **Partnerships for the Goals**
        - **Strengthen implementation through global partnerships**


        Use this space to make early learning fun and interactive.
        """)

       
        st.title("📘 Primary Learning Zone")
        st.markdown("### ✨ Choose a Language to Learn")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔤 English"):
                st.session_state.page = "english"

            
            
        with col2:
            if st.button("🌸 Kannada"):
                st.session_state.page = "kannada"
        with col3:
            if st.button("🪔 Hindi"):
                st.session_state.page = "hindi"

        st.markdown("---")
        if st.button("🔙 Back to Home"):
            st.session_state.page = "home"

    elif st.session_state.page == "english":
        st.title("🔤 English Alphabet Learning")
        st.markdown("### Click on a letter to learn how to write it")

        letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        for i in range(0, len(letters), 6):
            cols = st.columns(6)
            for j, col in enumerate(cols):
                if i + j < len(letters):
                    letter = letters[i + j]
                    if col.button(letter, use_container_width=True):
                        st.session_state.selected_letter = letter

        if "selected_letter" in st.session_state:
            selected = st.session_state.selected_letter
            if selected == "Q":
                st.image(
                    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.makeagif.com%2Fmedia%2F8-17-2020%2FsR_V2n.gif&f=1&nofb=1&ipt=bdd72401bd797fc4aa9957d80a510da0da4fa2b064424d35475da49e77f15e70",
                    caption="✍️ How to write 'Q'",
                    use_column_width=True
                )
                st.subheader("🔊 Hear how 'A' sounds")
                if st.button("▶️ Play Sound for Q"):
                    audio_file = open("q.mp3", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")
            elif selected == "A":
                st.image(
                    "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.makeagif.com%2Fmedia%2F6-02-2021%2FJKYoCQ.gif&f=1&nofb=1&ipt=da40fea9b77b4660dc0b7eca024571f7ae6ba06e5e2e0fc50566fc49ceb0818b",
                    caption="✍️ How to write 'A'",
                    use_column_width=True
                )
                st.subheader("🔊 Hear how 'A' sounds")
                if st.button("▶️ Play Sound for A"):
                    audio_file = open("a.mp3", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")

                
            else:
                st.info(f"📝 Animation for letter '{selected}' not available yet.")

        if st.button("🔙 Back to Primary"):
            st.session_state.page = "primary"
            st.session_state.selected_letter = None

    elif st.session_state.page == "kannada":
        st.title("🌸 Kannada Letters")
        st.markdown("""
        <div style='font-size: 56px; text-align: center; line-height: 2;'>
            <strong>ಸ್ವರಗಳು (Vowels)</strong><br>
            ಅ ಆ ಇ ಈ ಉ ಊ ಋ ೀ ಎ ಏ ಐ ಒ ಓ ಔ ಅಂ ಅಃ<br><br>
            <strong>ವ್ಯಂಜನಗಳು (Consonants)</strong><br>
            ಕ ಖ ಗ ಘ ಙ<br>
            ಚ ಛ ಜ ಝ ಞ<br>
            ಟ ಠ ಡ ಢ ಣ<br>
            ತ ಥ ದ ಧ ನ<br>
            ಪ ಫ ಬ ಭ ಮ<br>
            ಯ ರ ಲ ವ ಶ ಷ ಸ ಹ ಳ ಕ್ಷ ಜ್ಞ
        </div>
        """, unsafe_allow_html=True)

        kannada_letter = st.selectbox("📚 Choose a Kannada letter to learn:", ["", "ಅ", "ಆ"])

        if kannada_letter == "ಅ":
            st.image(
                "6b31f531f97a45998363f4f7425f4ade.gif",  # Example Kannada 'ಅ' writing gif
                caption="✍️ How to write 'ಅ'",
                use_column_width=True
            )
            st.subheader("🔊 Hear how 'ಅ' sounds")
            if st.button("▶️ Play Sound for ಅ"):
                audio_file = open("a_kannada.mp3", "rb")  # Ensure this file exists
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

        elif kannada_letter == "ಆ":
            st.image(
                "cc8bcca7f45442cc9aef9952cf9e449f.gif",  # Example Kannada 'ಆ' writing gif
                caption="✍️ How to write 'ಆ'",
                use_column_width=True
            )
            st.subheader("🔊 Hear how 'ಆ' sounds")
            if st.button("▶️ Play Sound for ಆ"):
                audio_file = open("aa_kannada.mp3", "rb")  # Ensure this file exists
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

        if st.button("🔙 Back to Primary"):
            st.session_state.page = "primary"

    elif st.session_state.page == "hindi":
        st.title("🨔 Hindi Letters")
        st.markdown("""
        <div style='font-size: 48px; text-align: center; line-height: 2;'>
            अ आ इ ई उ ऊ ऋ ए ऐ ओ औ अं अः<br>
            क ख ग घ ङ च छ ज झ ञ ट ठ ड ढ ण<br>
            त थ द ध न प फ ब भ म य र ल व श ष स ह
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔙 Back to Primary"):
            st.session_state.page = "primary"





elif nav_section == "Wallet":
    st.header("Wallet")
    st.write("Here you can view your total deposits and transaction history.")

    total_deposit = sum([entry['amount'] for entry in st.session_state.wallet])
    st.subheader(f"Total Deposited Amount: ₹ {total_deposit:.2f}")

    if st.session_state.wallet:
        st.write("### Deposit History")
        for idx, entry in enumerate(st.session_state.wallet, 1):
            st.write(f"{idx}. Amount: ₹{entry['amount']}, Date: {entry['timestamp']}")
    else:
        st.write("No deposits made yet.")

import streamlit as st

# Navigation section
if nav_section == "FAQ's":
    st.header("Sustainable Development Goals (SDG) Quiz 🌍")

    sdg_questions = [
        {
            "question": "1. What is the main aim of SDG 1?",
            "options": [
                "Zero Hunger",
                "No Poverty",
                "Quality Education",
                "Good Health and Well-being"
            ],
            "answer": "No Poverty"
        },
        {
            "question": "2. SDG 2 is focused on:",
            "options": [
                "Ending poverty",
                "Ensuring clean water",
                "Zero Hunger",
                "Climate action"
            ],
            "answer": "Zero Hunger"
        },
        {
            "question": "3. What does SDG 3 aim to achieve?",
            "options": [
                "Clean energy",
                "Innovation and infrastructure",
                "Healthy lives and well-being",
                "Reduced inequalities"
            ],
            "answer": "Healthy lives and well-being"
        },
        {
            "question": "4. Which goal ensures inclusive and equitable education?",
            "options": [
                "SDG 3",
                "SDG 4",
                "SDG 8",
                "SDG 5"
            ],
            "answer": "SDG 4"
        },
        {
            "question": "5. What is SDG 5 about?",
            "options": [
                "Gender Equality",
                "Sustainable cities",
                "Affordable energy",
                "Climate Action"
            ],
            "answer": "Gender Equality"
        },
        {
            "question": "6. SDG 6 promotes:",
            "options": [
                "Clean water and sanitation",
                "Economic growth",
                "Reduced inequalities",
                "Marine life protection"
            ],
            "answer": "Clean water and sanitation"
        },
        {
            "question": "7. Access to modern energy is targeted by:",
            "options": [
                "SDG 7",
                "SDG 10",
                "SDG 11",
                "SDG 16"
            ],
            "answer": "SDG 7"
        },
        {
            "question": "8. SDG 8 is about:",
            "options": [
                "Peace and justice",
                "Economic growth and decent work",
                "Climate change",
                "Life on land"
            ],
            "answer": "Economic growth and decent work"
        },
        {
            "question": "9. Innovation and infrastructure development falls under:",
            "options": [
                "SDG 5",
                "SDG 9",
                "SDG 4",
                "SDG 13"
            ],
            "answer": "SDG 9"
        },
        {
            "question": "10. Which SDG aims to reduce inequalities within and among countries?",
            "options": [
                "SDG 15",
                "SDG 13",
                "SDG 10",
                "SDG 2"
            ],
            "answer": "SDG 10"
        },
        {
            "question": "11. What is the focus of SDG 11?",
            "options": [
                "Sustainable cities and communities",
                "Life below water",
                "Gender Equality",
                "No poverty"
            ],
            "answer": "Sustainable cities and communities"
        },
        {
            "question": "12. What is SDG 12 about?",
            "options": [
                "Climate Action",
                "Responsible consumption and production",
                "Clean Water",
                "Peace and Justice"
            ],
            "answer": "Responsible consumption and production"
        },
        {
            "question": "13. Which SDG calls for urgent action to combat climate change?",
            "options": [
                "SDG 1",
                "SDG 13",
                "SDG 6",
                "SDG 8"
            ],
            "answer": "SDG 13"
        },
        {
            "question": "14. SDG 14 is focused on:",
            "options": [
                "Protecting life on land",
                "Clean energy",
                "Conserving life below water",
                "Gender equality"
            ],
            "answer": "Conserving life below water"
        },
        {
            "question": "15. What does SDG 15 focus on?",
            "options": [
                "Protecting terrestrial ecosystems",
                "Reducing plastic use",
                "Promoting innovation",
                "Inclusive education"
            ],
            "answer": "Protecting terrestrial ecosystems"
        },
        {
            "question": "16. SDG 16 promotes:",
            "options": [
                "Peace, justice and strong institutions",
                "Clean water",
                "Sustainable cities",
                "Gender equality"
            ],
            "answer": "Peace, justice and strong institutions"
        },
        {
            "question": "17. What is the aim of SDG 17?",
            "options": [
                "Promote global partnerships",
                "Improve health systems",
                "Promote agriculture",
                "Develop software"
            ],
            "answer": "Promote global partnerships"
        }
    ]

    # Session state initialization
    if "sdg_score" not in st.session_state:
        st.session_state.sdg_score = 0
        st.session_state.sdg_answers = [None] * len(sdg_questions)

    # Display each MCQ
    for i, q in enumerate(sdg_questions):
        st.subheader(q["question"])
        selected = st.radio("Choose one:", q["options"], key=f"sdg_q{i}", index=None)


        if st.session_state.sdg_answers[i] is None:
            if selected == q["answer"]:
                st.session_state.sdg_score += 1
            st.session_state.sdg_answers[i] = selected

    # Submit button
    if st.button("Submit SDG Quiz"):
        st.success(f"🎉 Your Score: {st.session_state.sdg_score} / {len(sdg_questions)}")

        if st.session_state.sdg_score == len(sdg_questions):
            st.balloons()
            st.markdown("### 🏅 SDG Mastery Badge Unlocked!")
        elif st.session_state.sdg_score >= len(sdg_questions) // 2:
            st.markdown("### 🥈 Great effort! You’ve got SDG knowledge.")
        else:
            st.markdown("### 💡 Keep learning and explore more about SDGs!")

        if st.button("🔄 Retake Quiz"):
            st.session_state.sdg_score = 0
            st.session_state.sdg_answers = [None] * len(sdg_questions)
            st.experimental_rerun()

#upgraded
if "footprint_data" not in st.session_state:
    st.session_state["footprint_data"] = {
        "transport_km": 0,
        "electricity_kwh": 0,
        "meat_meals": 0,
        "waste_kg": 0,
        "water_liters": 0,
    }

elif nav_section == "Support":
    st.header("Support")
    st.write("For assistance with the platform, please contact us at the following:")
    st.write("Email: support@secureplatform.com")
    st.write("Phone: +1-234-567-890")
    st.write("Our team is available 24/7 to assist you.")

    st.subheader("Carbon Footprint Tracker")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Transportation", "Electricity", "Diet", "Waste", "Water Usage"])

    with tab1:
        km = st.number_input("How many kilometers did you travel today (car/bike)?", min_value=0.0, step=0.1)
        st.session_state.footprint_data["transport_km"] = km

    with tab2:
        kwh = st.number_input("How many kWh of electricity did you use today?", min_value=0.0, step=0.1)
        st.session_state.footprint_data["electricity_kwh"] = kwh

    with tab3:
        meals = st.number_input("How many meat-based meals did you eat today?", min_value=0, step=1)
        st.session_state.footprint_data["meat_meals"] = meals

    with tab4:
        waste = st.number_input("How much waste did you generate today (in kg)?", min_value=0.0, step=0.1)
        st.session_state.footprint_data["waste_kg"] = waste

    with tab5:
        liters = st.number_input("How many liters of water did you use today?", min_value=0.0, step=1.0)
        st.session_state.footprint_data["water_liters"] = liters

    # Display Summary
    st.subheader("📊 24-Hour Usage Summary")
    st.write(f"🚗 **Transportation:** {st.session_state.footprint_data['transport_km']} km")
    st.write(f"⚡ **Electricity:** {st.session_state.footprint_data['electricity_kwh']} kWh")
    st.write(f"🍔 **Meat-based meals:** {st.session_state.footprint_data['meat_meals']}")
    st.write(f"🗑️ **Waste:** {st.session_state.footprint_data['waste_kg']} kg")
    st.write(f"🚿 **Water:** {st.session_state.footprint_data['water_liters']} liters")

    # Suggestions based on inputs
    st.subheader("💡 Suggestions to Reduce Your Carbon Footprint")

    if st.session_state.footprint_data["transport_km"] > 20:
        st.markdown("- Consider carpooling, biking, or using public transport for short trips.")
    else:
        st.markdown("- Great job keeping your travel minimal!")

    if st.session_state.footprint_data["electricity_kwh"] > 10:
        st.markdown("- Switch off unused appliances and try energy-efficient bulbs.")
    else:
        st.markdown("- Your electricity usage is within a good range!")

    if st.session_state.footprint_data["meat_meals"] > 2:
        st.markdown("- Try reducing meat consumption by adding plant-based meals.")
    else:
        st.markdown("- Balanced eating habits—keep it up!")

    if st.session_state.footprint_data["waste_kg"] > 1:
        st.markdown("- Reduce packaging waste and recycle regularly.")
    else:
        st.markdown("- Low waste generation—awesome!")

    if st.session_state.footprint_data["water_liters"] > 150:
        st.markdown("- Use low-flow faucets and be mindful during showers.")
    else:
        st.markdown("- You're using a responsible amount of water.")

    # Final Points
    st.subheader("🌍 Daily Eco-Points")
    points = 0
    if st.session_state["footprint_data"]["transport_km"] < 10:
        points += 2
    if st.session_state["footprint_data"]["electricity_kwh"] < 8:
        points += 2
    if st.session_state["footprint_data"]["meat_meals"] < 2:
        points += 2
    if st.session_state["footprint_data"]["waste_kg"] < 0.5:
        points += 2
    if st.session_state["footprint_data"]["water_liters"] < 100:
        points += 2

    st.success(f"🎯 You've earned **{points} / 10 Eco Points** today!")

elif nav_section == "Withdraw":
    st.header("Withdraw Funds")
    st.write("Here, you can withdraw funds from your wallet.")

    if st.session_state.wallet:
        total_balance = sum([entry['amount'] for entry in st.session_state.wallet])
        st.subheader(f"Available Balance: ₹ {total_balance:.2f}")

        withdraw_amount = st.number_input("Enter Amount to Withdraw:", min_value=0.0, max_value=total_balance, step=0.01)

        if st.button("Confirm Withdrawal"):
            if withdraw_amount <= total_balance:
                st.session_state.wallet.append({
                    "amount": -withdraw_amount,
                    "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                })
                st.success(f"The amount will be delivered within 24 hours, Withdraw request added ₹ {withdraw_amount:.2f}. Remaining Balance: ₹ {total_balance - withdraw_amount:.2f}")
            else:
                st.error("Insufficient balance!")
    else:
        st.write("No funds available in your wallet.")


elif nav_section == "Settings":
    st.header("Settings")
    st.write("Here, you can manage your account settings.")

    encryption_method = st.radio(
        "Select Encryption Method",
        options=["HE", "FFHE"],
        index=0 if st.session_state.encryption_method == "HE" else 1
    )
    if encryption_method != st.session_state.encryption_method:
        st.session_state.encryption_method = encryption_method
        st.success(f"Switched to {encryption_method} encryption method.")

elif nav_section == "Graph Chart":
    st.header("Transaction Chart")
    st.write("Here is a graphical representation of transaction amounts over time.")

    transaction_amounts = [float(transaction['transaction_amount']) for transaction in st.session_state.transaction_history]
    transaction_times = [time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) for _ in st.session_state.transaction_history]

    if transaction_amounts:
        fig, ax = plt.subplots()
        ax.bar(transaction_times, transaction_amounts, color='skyblue')
        ax.set_xlabel('Date and Time')
        ax.set_ylabel('Transaction Amount')
        ax.set_title('Transaction Amounts Over Time')
        st.pyplot(fig)
    else:
        st.write("No transactions to display in the graph.")

elif nav_section == "Spending Analysis":
    st.header("Spending Analysis")
    st.write("Here, you can analyze your spending patterns.")

    if st.session_state.wallet:
        total_spent = sum([entry['amount'] for entry in st.session_state.wallet])
        st.subheader(f"Total Spent: ₹ {total_spent:.2f}")

        spending_distribution = [entry['amount'] for entry in st.session_state.wallet]
        spending_labels = [f"Transaction {i+1}" for i in range(len(spending_distribution))]

        fig, ax = plt.subplots()
        ax.plot(spending_labels, spending_distribution, marker='o', color='orange', linestyle='-', linewidth=2)
        ax.set_xlabel('Transaction')
        ax.set_ylabel('Amount (₹)')
        ax.set_title('Spending Distribution Over Time')
        ax.grid(True)
        st.pyplot(fig)

        st.write("### Detailed Spending Table")
        st.table(st.session_state.wallet)

    else:
        st.write("No spending data available.")

elif nav_section == "Encrypted Data":
    st.header("Encrypted Transaction Data")
    st.write("Here is the encrypted data for each transaction.")

    if st.session_state.encrypted_transactions:
        for user_id, encrypted_data in st.session_state.encrypted_transactions.items():
            st.write(f"**User ID:** {user_id}, Encrypted Amount: {encrypted_data.ciphertext()}")
    else:
        st.write("No encrypted transactions yet.")


# Categories and news data
elif nav_section == "SDG News":
    # Categories and news data
    categories = ["Nature", "Automobile", "Education", "Health", "Technology", "Energy"]
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = "Nature"

    news_data = {
        "Nature": [
            {"title": "Amazon Rainforest Restoration Begins", "content": "Reforestation efforts are replanting over 1 million native trees in the Amazon to revive biodiversity."},
            {"title": "Ocean Cleanup Nets Record Plastic", "content": "20 tons of ocean plastic removed in the Pacific using new sustainable nets."},
            {"title": "Bee Populations Rebounding with Wildflower Corridors", "content": "Wildflower planting across farms is helping pollinators recover."},
            {"title": "Coral Reefs See Recovery Signs", "content": "Certain areas in the Great Barrier Reef have shown 30% coral regrowth after climate adaptation steps."},
            {"title": "Urban Forests Improve Air Quality", "content": "Cities adding green belts are seeing lower air pollution and better public health outcomes."},
        ],
        "Automobile": [
            {"title": "EV Sales Outpace Gas in EU", "content": "Electric vehicles outsold gas-powered cars in several EU countries last quarter."},
            {"title": "India Rolls Out E-Bike Highways", "content": "Dedicated highways for e-bikes aim to cut urban emissions."},
            {"title": "Self-Charging Cars in Testing", "content": "Solar charging panels integrated into car hoods are showing promising mileage boosts."},
            {"title": "Recycled Tires Now Standard in Green Cars", "content": "Tire manufacturers turn to fully recycled material for new electric cars."},
            {"title": "Battery Recycling Plants Open in Asia", "content": "New tech allows lithium batteries to be reused more efficiently."},
        ],
        "Education": [
            {"title": "SDG Curriculum in 1000 Schools", "content": "Rural schools get a sustainability-focused upgrade in classroom teaching."},
            {"title": "Digital Literacy for Girls Program Launched", "content": "New initiative trains girls in rural areas on digital tools for school and life."},
            {"title": "Mobile Libraries Reach Remote Villages", "content": "Books on wheels now deliver learning to mountain regions weekly."},
            {"title": "AI Tutors Being Piloted in Low-Income Areas", "content": "AI is helping students catch up in regions with teacher shortages."},
            {"title": "UNICEF Launches Climate Education App", "content": "New app lets children explore climate science through interactive games."},
        ],
        "Health": [
            {"title": "AI Assistants in Village Clinics", "content": "AI-driven health assistants are deployed in rural health posts to assist diagnosis."},
            {"title": "Free Sanitary Products in 300 Schools", "content": "Menstrual hygiene program launches in partnership with local health units."},
            {"title": "Nutrition Campaigns Reduce Child Stunting", "content": "Awareness drives and food packs are improving child health indicators."},
            {"title": "Telemedicine Vans Launched", "content": "Doctors can now reach remote patients via mobile consultation units."},
            {"title": "Malaria Vaccine Trials Expand", "content": "Africa leads the way in a new malaria vaccine showing 70% success."},
        ],
        "Technology": [
            {"title": "Blockchain for Transparent Aid", "content": "Aid organizations now track donations via blockchain to ensure zero corruption."},
            {"title": "AI Waste Sorting Deployed in Cities", "content": "Smart bins separate trash using AI to improve recycling."},
            {"title": "Low-Cost Solar Drones to Deliver Supplies", "content": "Startups build drones to drop essentials in disaster-hit villages."},
            {"title": "Open-Source Climate Simulators Released", "content": "Free tools help students visualize climate change impacts in their regions."},
            {"title": "Rural Internet Towers Installed", "content": "Off-grid towers powered by wind and sun connect isolated communities."},
        ],
        "Energy": [
            {"title": "Wind Farms Expand Along Coast", "content": "New wind farms power 100,000 rural homes across India."},
            {"title": "Affordable Solar Kits for Farmers", "content": "Irrigation pumps and grain mills now run on portable solar panels."},
            {"title": "Bioenergy from Agricultural Waste Rising", "content": "Farm waste gets converted into clean-burning gas for home use."},
            {"title": "India’s Largest Hydroelectric Plant Opens", "content": "Hydro project powers 3 states while reducing flood risks."},
            {"title": "Community Energy Cooperatives Take Off", "content": "Villagers now co-own microgrids supplying renewable power locally."},
        ]
    }

    # Render category buttons
    cols = st.columns(len(categories))
    for i, category in enumerate(categories):
        if cols[i].button(category):
            st.session_state.selected_category = category

    # Show articles for selected category
    st.markdown(f"### 📰 {st.session_state.selected_category} News")
    for article in news_data[st.session_state.selected_category]:
        with st.expander(article["title"]):
            st.write(article["content"])



elif nav_section == "Logout":
    st.session_state.user_authenticated = False
    st.session_state.user_id = ""
    st.session_state.pan_no = ""
    st.session_state.encrypted_transactions = {}
    st.session_state.transaction_history = []
    st.session_state.wallet = []

    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Fake AR</title>
      <style>
        body, html {
          margin: 0;
          overflow: hidden;
          background: black;
        }
        #camera {
          position: fixed;
          top: 0; left: 0;
          width: 100vw;
          height: 100vh;
          object-fit: cover;
          z-index: 0;
        }
        #overlayVideo {
          position: fixed;
          top: 20%;
          left: 20%;
          width: 60vw;
          z-index: 1;
          pointer-events: none;
          border-radius: 12px;
          box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
      </style>
    </head>
    <body>
      <video id="camera" autoplay playsinline muted></video>
      <video id="overlayVideo" autoplay loop muted>
        <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">

        Your browser does not support the video tag.
      </video>

      <script>
        const camera = document.getElementById('camera');
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            camera.srcObject = stream;
          })
          .catch(err => {
            console.error("Camera access failed:", err);
          });
      </script>
    </body>
    </html>
    """

    st.markdown("### 🎥 AR Experience")
    components.html(html_code, height=700, scrolling=False)
#all tabs done
    
#challenge completed
