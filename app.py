import streamlit as st
import time
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

# ------------------ SESSION STATE INIT ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}
    ]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# ------------------ DETECT "I am Del" FLEXIBLY ------------------ #
def detect_del_identity(text):
    text = text.lower()
    return "del" in text and any(phrase in text for phrase in ["i am", "i'm", "me", "mai", "main"])

# ------------------ APPLY WHITE THEME IF DEL ------------------ #
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stChatMessage, .stTextInput, .stTextArea {
            border: 1px solid #222 !important;
            border-radius: 6px;
        }
        .css-1cpxqw2, .stTextInput>div>div>input {
            background-color: #f6f6f6 !important;
            color: black !important;
            border: 1px solid #222 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Built on Gemini. Expect Hinglish, sarcasm, tech gyaan, and mood swings.")

# ------------------ SHOW CHAT HISTORY ------------------ #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------ #
if user_input := st.chat_input("Message DelGPT..."):

    # First: detect Del mode before doing anything else
    if not st.session_state.is_del and detect_del_identity(user_input):
        st.session_state.is_del = True

    # Show + save user input
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Prepare Gemini prompt using Del persona
    prompt = get_del_prompt(user_input)

    # Get response from Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            del_response = get_gemini_response(prompt)
        except Exception as e:
            del_response = f"❌ Error aagya bhai — {str(e)}"

        for word in del_response.split():
            full_response += word + " "
            time.sleep(0.035)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Store bot response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
