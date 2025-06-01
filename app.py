import streamlit as st
import time
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

# Page config
st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}
    ]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# Detect identity
def detect_del_identity(text):
    text = text.lower()
    return "del" in text and any(x in text for x in ["i am", "i'm", "mai", "main", "me"])

# Theme switch
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stTextInput>div>div>input {
            background-color: #f2f2f2 !important;
            color: #000 !important;
            border: 1px solid #222 !important;
        }
        .message-container {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 12px;
            background-color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Built on Gemini. Expect Hinglish, sarcasm, tech gyaan, and mood swings.")

# Render all messages manually
for msg in st.session_state.messages:
    avatar = "public/del_avatar.png" if msg["role"] == "assistant" else None
    with st.container():
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 10px;" class="message-container">
            {'<img src="' + avatar + '" width="40" style="border-radius: 50%;" />' if avatar else ''}
            <div>{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

# Handle new user message
if user_input := st.chat_input("Message DelGPT..."):

    if not st.session_state.is_del and detect_del_identity(user_input):
        st.session_state.is_del = True

    st.session_state.messages.append({"role": "user", "content": user_input})

    prompt = get_del_prompt(user_input)

    with st.container():
        st.markdown(f"""
        <div style="display: flex; align-items: flex-start; gap: 10px;" class="message-container">
            <img src="public/del_avatar.png" width="40" style="border-radius: 50%;" />
            <div id="del-output">
        """, unsafe_allow_html=True)

        placeholder = st.empty()
        full_response = ""

        try:
            response = get_gemini_response(prompt)
        except Exception as e:
            response = f"❌ Error aagya bhai — {str(e)}"

        for word in response.split():
            full_response += word + " "
            time.sleep(0.03)
            placeholder.markdown(full_response + "▌")
        placeholder.markdown(full_response)

        st.markdown("</div></div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
