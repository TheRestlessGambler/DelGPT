import streamlit as st
import time
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

# ---- Session State Init ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}
    ]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# ---- Check if user says "I'm Del" in this session ----
def detect_del_identity(msg):
    triggers = ["i am del", "i'm del", "me del", "mai del", "main del hoon"]
    return any(trigger in msg.lower() for trigger in triggers)

# ---- White Theme CSS (Triggered when user says "I am Del") ----
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .css-1cpxqw2, .css-13sdm1v, .css-1y4p8pa, .stTextInput>div>div>input {
            background-color: #f6f6f6 !important;
            color: black !important;
            border: 1px solid #222 !important;
        }
        .stChatMessage, .stTextInput, .stTextArea {
            border: 1px solid #aaa !important;
            border-radius: 6px;
        }
        .stTextInput>div>div, .stTextArea>div>div {
            background-color: #fdfdfd !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ---- Title ----
st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Gemini-powered chatbot. Expect Hinglish, sarcasm, tech obsessions & zero patience.")

# ---- Show Messages ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat Input ----
if user_input := st.chat_input("Message DelGPT..."):
    # Trigger Del mode if user identifies as Del
    if not st.session_state.is_del and detect_del_identity(user_input):
        st.session_state.is_del = True

    # Show and save user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate DelGPT reply
    prompt = get_del_prompt(user_input)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            del_response = get_gemini_response(prompt)
        except Exception as e:
            del_response = f"❌ Error aagya bhai — {str(e)}"
        
        # Simulate typing effect
        for word in del_response.split():
            full_response += word + " "
            time.sleep(0.035)
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
